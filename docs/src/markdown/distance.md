# Color Distance and Delta E

ColorAide Extras not only includes some experimental color spaces, but includes some associated ∆E methods as well.

## CAM16

The CAM16 UCS color space is perceptually uniform. Part of the reason for its creation is to help improve color
distancing. CAM02, which CAM16 is based off of and meant to improve, specified 3 color spaces: UCS, LCD, and SCD. LCD
and SCD are particular for large scale and small scale color differencing respectively.

Our implementation of CAM16 also implements UCS, LCD and SCD color spaces and provides a color distancing method called
`cam16` which utilizes the aforementioned color spaces. By default the method utilizes the CAM16 UCS color space, but
if `magnitude` is specified with either `lcd` or `scd`, the appropriate CAM16 LCD or CAM16 SCD color space will be used
instead (assuming all required color spaces are registered).

```playground
Color('red').delta_e('blue', method='cam16')
Color('red').delta_e('blue', method='cam16', magnitude='scd')
Color('red').delta_e('blue', method='cam16', magnitude='lcd')
```
