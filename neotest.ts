{
    let strip = neopixel.create(1, 24, NeoPixelMode.RGB);
    strip.setPixelColor(0, 0xff0000)
    strip.setPixelColor(1, 0x00ff00)
    strip.setPixelColor(2, 0x0000ff)
    strip.show()
    pause(2000)
    strip.showRainbow();
    for (let i = 0; i <= strip.length(); i++) { 
        strip.rotate();
        strip.show();
        pause(100)
    }
    
    strip.showColor(NeoPixelColors.Red)
    pause(2000)
    strip.showColor(NeoPixelColors.Green)
    pause(1000)
    for (let i = 0; i <= strip.length(); i++) {
        strip.setPixelColor(i, neopixel.colors(NeoPixelColors.Blue))
        strip.show()
        pause(100)
    }
    for (let i = 0; i <= strip.length(); i++) {
        strip.setPixelColor(i, neopixel.colors(NeoPixelColors.Green))
        strip.show()
        pause(100)
    }
    let sub = strip.range(10, 20)
    sub.showColor(NeoPixelColors.Yellow);
    pause(200);

    sub.showBarGraph(5, 10);
    pause(200);

    strip.setMatrixWidth(8);
    strip.setMatrixColor(0, 0, NeoPixelColors.Red);
    strip.setMatrixColor(1, 1, NeoPixelColors.Green);
    strip.show();
    pause(200);

    strip.easeBrightness();
    strip.show();
    pause(200);

    let p = strip.power();

    let br = 100;
    strip.setBrightness(100);
    const _this = (strip as any);
    const _input = _this["input"];
    if (_input) {
        _input.onButtonPressed(2 /* Button.B */, () => {
            br = br + 20;
            if (br > 255) {
                br = 5;
            }
            strip.setBrightness(br);
        });
    }

    let rotationMode = false;
    if (_input) {
        _input.onButtonPressed(1 /* Button.A */, () => {
            rotationMode = !rotationMode;
            const _basic = _this["basic"];
            if (rotationMode && _basic && _basic.showLeds) {
                _basic.showLeds(`
                . # # # .
                # . . . #
                # . . . #
                # . . . #
                . # # # .
                `);
            } else if (_basic && _basic.showLeds) {
                _basic.showLeds(`
                . . # . .
                . . . # .
                # # # # #
                . . . # .
                . . # . .
                `);

            }
        });
    }

    while (true) {
        let x = 0;
        let y = 0;
        let z = 0;
        if (_input && _input.acceleration) {
            x = _input.acceleration(0 /* Dimension.X */) >> 1
            y = _input.acceleration(1 /* Dimension.Y */) >> 1
            z = _input.acceleration(2 /* Dimension.Z */) >> 1
        }
        if (rotationMode) {
            strip.rotate();
        } else {
            strip.setPixelColor(0, neopixel.rgb(x, y, -z));
            strip.shift(1);
        }
        strip.show();
        pause(100);
    }
}
