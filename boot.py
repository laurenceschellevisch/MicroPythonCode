# import settings
# from network import WLAN

# wlan = WLAN(mode=WLAN.STA)
# nets = wlan.scan()  # Scan all SSID networks
# print('WLAN init')
# for net in nets:
#     print(net)
#     if net.ssid == settings.wifi_ssid:
#         wlan.connect(net.ssid, auth=(
#             net.sec, settings.wifi_password), timeout=5000)
#         while not wlan.isconnected():
#             machine.idle()  # Save power while waiting
#         print('WLAN connection succeeded!')
#         break
