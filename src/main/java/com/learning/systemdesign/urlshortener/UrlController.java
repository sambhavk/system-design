package com.learning.systemdesign.urlshortener;

import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
@RequestMapping("/v1/url")
public class UrlController {

    public final UrlProcessor urlProcessor;

    @PostMapping("/shorten")
    public ResponseEntity<String> shortenUrl(@RequestBody String url){
        return ResponseEntity.ok(urlProcessor.shortenUrl(url));
    }

}
