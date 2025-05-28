from shapely import wkt, wkb

def validate_wkt(wkt_str: str):
    try:
        return wkt.loads(wkt_str)
    except Exception:
        raise ValueError("Invalid WKT format")

def wkb_to_wkt(wkb_data) -> str:
    geom = wkb.loads(bytes(wkb_data))
    return geom.wkt

def wkb_to_xy(wkb_data) -> dict:
    geom = wkb.loads(bytes(wkb_data))
    return {"x": geom.x, "y": geom.y}
