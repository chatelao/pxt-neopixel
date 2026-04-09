# NeoPixel Implementation in MakeCode Adafruit

This document summarizes the NeoPixel support in the Adafruit MakeCode platform (https://makecode.adafruit.com).

## Overview
The Adafruit MakeCode platform provides built-in support for NeoPixels through the `light` namespace. This is distinct from the standalone `neopixel` extension found in this repository, although they share some history and conceptual similarities.

## Does it use this library?
**No**, the primary NeoPixel support in MakeCode Adafruit does not use this specific `microsoft/pxt-neopixel` library as its core implementation. Instead, it uses a more integrated `light` library (found in the `pxt-common-packages` repository under `libs/light`).

However, the `neopixel` extension from this repository can still be added to MakeCode Adafruit projects as an external extension. Interestingly, the `light` library in MakeCode Adafruit includes deprecated aliases for several `neopixel` blocks to maintain compatibility with older projects that might have used the original `neopixel` extension.

## Included Libraries

### 1. The `light` Library (Built-in)
The `light` library is the native way to control LEDs in MakeCode Adafruit. It supports:
- **Onboard LEDs:** Built-in support for the NeoPixel ring on the Circuit Playground Express.
- **External Strips:** Created via `light.createStrip()`.
- **Animations:** A rich set of built-in animations like Rainbow, Sparkle, and Comet.
- **Photon Effect:** A unique "photon" cursor that can move along the strip, leaving a trail.
- **Additional Hardware:** Support for APA102 LEDs in addition to WS2812B (NeoPixels).

### 2. The `neopixel` Extension (External)
The `pxt-neopixel` extension (this repository) can be manually added. It is simpler and more focused on basic strip operations. It is the same library used in MakeCode for micro:bit.

## Key Differences

| Feature | `light` (Adafruit Built-in) | `neopixel` (This Library) |
| --- | --- | --- |
| **Namespace** | `light` | `neopixel` |
| **Primary Target** | Circuit Playground Express | micro:bit, Calliope, Maker |
| **Animations** | Many built-in (Rainbow, Comet, etc.) | Limited (Rainbow, Bar Graph) |
| **Buffering** | Optional (`setBuffered`) | Built-in (requires `show()`) |
| **Advanced Features** | Photon effect, HSL/HSV, transitions | Basic HSL, Bar Graph |
| **LED Types** | WS2812B, RGBW, APA102 | WS2812B, RGBW |

## Summary
While MakeCode Adafruit has its own highly optimized and feature-rich `light` library for NeoPixel control, it maintains a level of compatibility with the `neopixel` library. The `neopixel` library remains the standard for micro:bit and other targets, while Adafruit users are generally encouraged to use the built-in `light` blocks.
