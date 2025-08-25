import pathlib
import sys
import typing

import click
import PIL.Image
import PIL.ImageOps
import qrcode
import qrcode.constants
from qrcode.image.styledpil import StyledPilImage
from click_option_group import optgroup, MutuallyExclusiveOptionGroup, MutuallyExclusiveOptionGroup

def _shared_args(wrapped):
    @optgroup("Data", cls=MutuallyExclusiveOptionGroup)
    @optgroup.option("--data", help="The data to encode")
    @optgroup.option("--data-file")
    @click.option("--back-color", help="The background color to make the qr code", default="white")
    @click.option("--out", type=click.Path(path_type=pathlib.Path, dir_okay=False))
    def wrapper(*args, **kwargs):
        return wrapped(*args, **kwargs)
    
    return wrapper

@click.group(invoke_without_command=True)
@click.option(
    "--logo",
    help="The logo to use in the QR code",
    type=click.Path(path_type=pathlib.Path, exists=True, dir_okay=False),
)
@click.option(
    "--logo-ratio",
    help="The 1/nth of the size of the image to make the logo.",
    type=click.FloatRange(min=3),
    default=3,
)
@click.option("--color", help="The color to make the qr code", default="black")
@_shared_args
def _cli(
    data: str,
    logo: typing.Optional[pathlib.Path],
    logo_ratio: int,
    color: str,
    back_color: str,
    out: pathlib.Path,
    data_file: typing.Optional[str],
):
    """Create a branded QR code based on parameters.

    --data or DATA_FILE must be passed. if DATA_FILE is a '-', then stdin is read.
    """
    if not ((data is None) ^ (data_file is None)):
        raise click.BadArgumentUsage("Exactly one of --data or DATA_FILE must be passed.")
    if data_file:
        data_lines = []
        if data_file == "-":
            for line in sys.stdin.read():
                data_lines.append(line)
            data = "\n".join(data_lines)
        else:
            data = pathlib.Path(data_file).read_text(encoding="UTF-8-sig")

    QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)

    QRcode.add_data(data)
    QRcode.make()

    quick_response_image = QRcode.make_image(fill_color=color, back_color=back_color).convert("RGB")

    quick_response_image = quick_response_image.resize((1024, 1024))

    if logo:
        logo_img = PIL.Image.open(logo)
        if logo_img.size[0] > quick_response_image.size[0] // logo_ratio:
            ratio = logo_ratio
            logo_img = PIL.ImageOps.contain(
                logo_img,
                (
                    int(quick_response_image.size[0] / ratio),
                    int(quick_response_image.size[1] / ratio),
                ),
            )
        pos = (
            (quick_response_image.size[0] - logo_img.size[0]) // 2,
            (quick_response_image.size[1] - logo_img.size[1]) // 2,
        )
        quick_response_image.paste(logo_img, pos)

    quick_response_image.save(out)


if __name__ == "__main__":
    _cli()
