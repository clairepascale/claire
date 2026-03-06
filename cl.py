import base64
import random
import requests
from seleniumbase import SB

# -----------------------------
# GEO / LOCALE CONFIG
# -----------------------------
geo_data = requests.get("http://ip-api.com/json/").json()

latitude = geo_data["lat"]
longitude = geo_data["lon"]
timezone_id = geo_data["timezone"]
language_code = geo_data["countryCode"].lower()

proxy_str = False

# -----------------------------
# TARGET CHANNEL
# -----------------------------
name = "YnJ1dGFsbGVz"
fulln = base64.b64decode(name).decode("utf-8")
urlt = f"https://www.twitch.tv/{fulln}"

# -----------------------------
# MAIN LOOP
# -----------------------------
while True:
    with SB(
        uc=True,
        locale="en",
        ad_block=True,
        chromium_arg="--disable-webgl",
        proxy=proxy_str
    ) as xacasa:

        rnd = random.randint(450, 800)

        # Activate CDP with geolocation + timezone
        xacasa.activate_cdp_mode(
            urlt,
            tzone=timezone_id,
            geoloc=(latitude, longitude)
        )

        xacasa.sleep(2)

        # Accept cookies
        if xacasa.is_element_present('button:contains("Accept")'):
            xacasa.cdp.click('button:contains("Accept")', timeout=4)

        xacasa.sleep(12)

        # Start watching if needed
        if xacasa.is_element_present('button:contains("Start Watching")'):
            xacasa.cdp.click('button:contains("Start Watching")', timeout=4)
            xacasa.sleep(10)

        # Accept again if appears
        if xacasa.is_element_present('button:contains("Accept")'):
            xacasa.cdp.click('button:contains("Accept")', timeout=4)

        # -----------------------------
        # CHECK IF LIVE STREAM EXISTS
        # -----------------------------
        if xacasa.is_element_present("#live-channel-stream-information"):

            # Accept again if needed
            if xacasa.is_element_present('button:contains("Accept")'):
                xacasa.cdp.click('button:contains("Accept")', timeout=4)

            # -----------------------------
            # SECOND DRIVER
            # -----------------------------
            xacasa2 = xacasa.get_new_driver(undetectable=True)
            xacasa2.activate_cdp_mode(
                urlt,
                tzone=timezone_id,
                geoloc=(latitude, longitude)
            )

            xacasa2.sleep(10)

            if xacasa2.is_element_present('button:contains("Start Watching")'):
                xacasa2.cdp.click('button:contains("Start Watching")', timeout=4)
                xacasa2.sleep(10)

            if xacasa2.is_element_present('button:contains("Accept")'):
                xacasa2.cdp.click('button:contains("Accept")', timeout=4)

            # -----------------------------
            # WATCH TIME
            # -----------------------------
            xacasa.sleep(rnd)

        else:
            # Stream not live → exit loop
            break
