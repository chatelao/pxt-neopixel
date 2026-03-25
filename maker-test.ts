{
    let pin: any = 1;
    let strip = neopixel.create(pin, 10, NeoPixelMode.RGB);
    strip.setPixelColor(0, NeoPixelColors.Red);
    strip.setPixelColor(1, NeoPixelColors.Green);
    strip.setPixelColor(2, NeoPixelColors.Blue);
    strip.show();

    strip.showRainbow(1, 360);
    for (let i = 0; i < 10; i++) {
        strip.rotate(1);
        strip.show();
        pause(100);
    }

    strip.clear();
    strip.show();
}
