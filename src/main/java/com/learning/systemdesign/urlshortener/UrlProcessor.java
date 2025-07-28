package com.learning.systemdesign.urlshortener;

import org.springframework.stereotype.Service;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;

import static com.learning.systemdesign.urlshortener.Constants.*;

@Service
public class UrlProcessor {

    public String shortenUrl(String url) {
        try {
            // Step 1: Hash the URL using SHA-256
            MessageDigest sha256 = MessageDigest.getInstance("SHA-256");
            byte[] hashBytes = sha256.digest(url.getBytes(StandardCharsets.UTF_8));

            // Step 2: Convert first 6 bytes to long (48 bits, fits well for base62)
            long number = 0;
            for (int i = 0; i < 6; i++) {
                number = (number << 8) | (hashBytes[i] & 0xFF);
            }

            // Step 3: Base62 encode the number
            StringBuilder sb = new StringBuilder();
            while (number > 0) {
                int remainder = (int) (number % CHARSET.length());
                sb.append(CHARSET.charAt(remainder));
                number /= CHARSET.length();
            }

            // Step 4: Pad or trim to exactly 8 characters
            while (sb.length() < TARGET_LENGTH) {
                sb.append('0');
            }

            return BASE_URL + sb.reverse().substring(0, TARGET_LENGTH);
        } catch (Exception e) {
            throw new RuntimeException("Error generating short URL", e);
        }
    }

}
