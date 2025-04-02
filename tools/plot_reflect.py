"""Spectral curve plots."""
import sys
import os
import argparse
import plotly.graph_objects as go
import plotly.io as io

sys.path.insert(0, os.getcwd())

from coloraide_extras.interpolate import spectral
from coloraide import algebra as alg
from coloraide.everything import ColorAll as Color

START = 380
STEP = 10
END = 750 + STEP
WL = list(range(START, END, STEP))

def main():
    """Main."""

    parser = argparse.ArgumentParser(prog='plot_reflect', description='Plot reflectance of a given color.')
    parser.add_argument('--color', '-c', action='append', help="Color.")
    parser.add_argument('--title', '-T', default='', help="Title of plot")
    parser.add_argument('--mix', '-m', type=float, default=0.5, help="Mix percentage")
    parser.add_argument('--decomp', '-d', action="store_true", help='Show color decompossed into RGB.')
    parser.add_argument('--resolution', '-r', default="800", help="How densely to render the figure.")
    parser.add_argument('--no-border', '-b', action="store_true", help='Draw no border around the graphed content.')
    parser.add_argument('--dark', action="store_true", help="Use dark theme.")
    parser.add_argument('--dpi', default=200, type=int, help="DPI of image.")
    parser.add_argument('--output', '-o', default='', help='Output file.')

    args = parser.parse_args()

    colors = args.color

    style = []

    if len(colors) < 1 or len(colors) > 2:
        raise ValueError(f'Need 1 - 2 colors, not {len(colors)}')

    if len(colors) == 1:
        color = Color(args.color[0])
        xyz = color.convert('xyz-d65')[:-1]
        c = spectral.xyz_to_concentration(xyz)
        r, res1 = spectral.single_constant_xyz_to_reflectance(xyz)

        style = ['solid']
        target = [r]
        plot = [color.convert('srgb').to_string(hex=True)]

        if args.decomp:
            target.append([ri * c[0] for ri in spectral.REF_C])
            target.append([ri * c[1] for ri in spectral.REF_M])
            target.append([ri * c[2] for ri in spectral.REF_Y])
            target.append([ri * c[3] for ri in spectral.REF_R])
            target.append([ri * c[4] for ri in spectral.REF_G])
            target.append([ri * c[5] for ri in spectral.REF_B])
            plot.extend(['#00ffff', '#ff00ff', '#ffff00', '#ff0000', '#00ff00', '#0000ff'])
            style.extend(['dash'] * 6)
    else:
        color = Color(args.color[0])
        xyz = color.convert('xyz-d65')[:-1]
        color2 = Color(args.color[1])
        xyz2 = color2.convert('xyz-d65')[:-1]
        r1, res1 = spectral.single_constant_xyz_to_reflectance(xyz)
        r2, res2 = spectral.single_constant_xyz_to_reflectance(xyz2)

        # Apply the Kubelka-Munk mixing
        target = []
        plot = []
        count = 0
        for i in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, args.mix):
            t = spectral.nonlinear_luminance_ease(xyz[1], xyz2[1], i)
            size = len(r1)
            r = [0.0] * size
            for i in range(size):
                ks1 = (1 - r1[i]) ** 2 / (2 * r1[i])
                ks2 = (1 - r2[i]) ** 2 / (2 * r2[i])

                # Perform the actual interpolation
                ks = alg.lerp(ks1, ks2, t)

                r[i] = (1 + ks - alg.nth_root(ks ** 2 + 2 * ks, 2))

            if count != 9:
                target.append(r)
                plot.append('#cccccc')
                style.append('dash')
            else:
                target.append(r)
                xyz1 = spectral.reflectance_to_xyz(r)
                xyz2 = [alg.lerp(r1, r2, t) for r1, r2 in zip(res1, res2)]
                xyz_final = [xyz1[0] + xyz2[0], xyz1[1] + xyz2[1], xyz1[2] + xyz2[2]]
                color3 = Color('xyz-d65', xyz_final)
                plot.append(color3.convert('srgb').to_string(hex=True))
                style.append('solid')

            count += 1

        target.append(r1)
        target.append(r2)
        plot.append(color.convert('srgb').to_string(hex=True))
        plot.append(color2.convert('srgb').to_string(hex=True))
        style.extend(['solid'] * 2)

    # Create titles
    title = args.title
    if not title:
        title = f'Reflectance Curve of {color.to_string()}'
        if not color.in_gamut('srgb'):
            if len(args.color()) == 1:
                title += '<br><sup>Color out of sRGB gamut, curves may be attenuated</sup>'
            else:
                title = f'Spectral mix of {color.to_string()} and {color2.to_string()}'

    fig = go.Figure(
        layout={
            'title': title,
            'xaxis_title': 'Wavelength',
            'yaxis_title': 'Reflection'
        }
    )

    for e, data in enumerate(zip(plot, target)):
        p, t = data

        fig.add_traces(data=go.Scatter(
            x=list(range(START, END, STEP)),
            y=t,
            mode="lines",
            line={'color': p, 'width': 2, 'dash': style[e]},
            showlegend=False
        ))

    if fig:
        if args.output:
            filetype = os.path.splitext(args.output)[1].lstrip('.').lower()
            if filetype == 'html':
                with open(args.output, 'w') as f:
                    f.write(io.to_html(fig))
            elif filetype == 'json':
                io.write_json(fig, args.output)
            else:
                with open(args.output, 'wb') as f:
                    f.write(fig.to_image(format=filetype))
        else:
            fig.show()
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
