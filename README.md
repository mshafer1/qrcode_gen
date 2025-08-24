# QRCode-gen

A Python script to take the [`qrcode`](https://pypi.org/project/qrcode/) module and provide a convenient CLI with advanced options.

NOTE: always test your QR codes, this tool does not garauntee that the resulting QR code will work (See [License](https://github.com/mshafer1/qrcode_gen/blob/main/LICENSE))

# Example 1, URL:

```
poetry run qr-codes --logo "logo_file.png" --data https://example.com --out example.com.qr.png
```

# Example 2, URL with smaller logo:

The size of the logo to the rest defaults to 1/3. Specifying `--logo-ratio 4` changes this to 1/4.

Note that if the logo is not perfectly square, the larger dimension is used to determine the bounding box.

```
poetry run qr-codes --logo "logo_file.png" --logo-ratio 4 --data https://example.com --out example.com.qr.png
```

# Example 3, Wi-FI:

See [the spec](https://web.archive.org/web/20250404113245if_/https://www.wi-fi.org/system/files/WPA3%20Specification%20v3.2.pdf#page=25)

for more details


```
poetry run qr-codes --logo "logo_file.png" --data WIFI:T:WPA;S:Wif-name-here;P:wifi-password-here;M:false;; --out wifi.qr.png
```
