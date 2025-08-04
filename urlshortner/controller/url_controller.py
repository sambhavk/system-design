from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from urlshortner.dto.url_shorten_request import UrlShortenRequest
from urlshortner.service.url_service import UrlService

router = APIRouter()


@router.post("/v1/url/shorten")
async def shorten_url_api(req: UrlShortenRequest):
    shortened = await UrlService.shorten_url(req)
    return {"shortened_url": f"http://url-shortener/{shortened}"}


@router.get("/v1/url/{shortened_url}")
async def redirect_api(shortened_url: str):
    original = await UrlService.redirect_url(shortened_url)
    if not original:
        raise HTTPException(status_code=404, detail="Shortened URL not found or expired")
    return RedirectResponse(url=original, status_code=302)
