import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import uuid
import cartopy.crs as ccrs
from cartopy.mpl.geoaxes import GeoAxes



def axes(projection: ccrs.Projection) -> GeoAxes:
    return plt.axes(projection=projection)


def geoaxes(
    num: int | Figure = None,
    projection: ccrs.Projection = ccrs.PlateCarree(),
    figsize: tuple[float, float] = (6, 9),
) -> tuple[Figure, GeoAxes]:

    fig = plt.figure(num if num else uuid.uuid1(), figsize=figsize)

    ax: GeoAxes = axes(projection=projection)

    gl = ax.gridlines(
        crs=projection,
        draw_labels=True,
        linewidth=0.5,
        color="gray",
        alpha=0.5,
        linestyle="--",
    )

    gl.top_labels = False

    gl.right_labels = False

    ax.coastlines(resolution="auto")

    return fig, ax
