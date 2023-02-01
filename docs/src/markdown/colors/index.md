# Supported Color Spaces

ColorAide Extras adds a number of additional color spaces to ColorAide. Some are just spaces that are less practical
to use for common cases, some are just interesting for specific applications, some are implemented just for history,
and some are fairly new and a bit experimental.

Click a color space to learn more.

```diagram
flowchart TB

    cam16-ucs --- xyz-d65
        cam16-ucs-jmh --- cam16-ucs

    ucs --- xyz-d65
    uvw --- xyz-d65
    hct --- xyz-d65

    xyz-d65(XYZ D65)
    cam16-ucs(CAM16 UCS)
    cam16-ucs-jmh(CAM16 UCS JMh)
    hct(HCT)
    ucs(CIE 1960 UCS)
    uvw(CIE 1964 UVW)

    click xyz-d65 "https://facelessuser.github.io/coloraide/colors/xyz_d65/" _blank
    click cam16-ucs "./cam16_ucs/" _self
    click cam16-ucs-jmh "./cam16_ucs_jmh/" _self
    click hct "./hct/" _self
    click ucs "./ucs/" _self
    click uvw "./uvw" _self
```
