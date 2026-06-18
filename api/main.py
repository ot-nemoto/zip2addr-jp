from fastapi import FastAPI, Path
from fastapi.responses import JSONResponse

from zip2addr import __version__, lookup

app = FastAPI(
    title="zip2addr-jp API",
    description="日本の郵便番号から住所を検索する REST API",
    version=__version__,
)


@app.get("/api/v1/address/{postal_code}")
def get_address(
    postal_code: str = Path(..., description="郵便番号（ハイフン有無、全半角対応）"),
):
    results = lookup(postal_code)
    if not results:
        return JSONResponse(
            status_code=404,
            content={"detail": "該当する住所が見つかりません"},
        )
    return [r.to_dict() for r in results]


@app.get("/api/v1/health")
def health():
    return {"status": "ok", "version": __version__}
