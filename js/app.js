import axios from 'axios';

var colors = ['#FFFFFF', '#E4E4E4', '#888888','#222222',
              '#FFA7D1','#E50000','#E59500', '#A06A42',
              '#E5D900','#94E044','#02BE01','#00E5F0',
              '#0083C7','#0000EA','#E04AFF','#820080'];
function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}

function paintPixel(ctx, x, y, hex){
    var pixel = ctx.createImageData(1, 1);
    for (var i = 0; i < pixel.data.length; i += 4) {
            var rgb = hexToRgb(hex);
            pixel.data[i+0] = rgb.r;
            pixel.data[i+1] = rgb.g;
            pixel.data[i+2] = rgb.b;
            pixel.data[i+3] = 255;
        }
    ctx.putImageData(pixel, x, y);
}


var c = document.getElementById("place");
var ctx = c.getContext("2d");
var start = 1490980000;

function nextSecond(){
    axios.get('http://127.0.0.1:5000/?start=' + start + "&end=" + (start + 60))
    .then(function (resp) {
        resp.data.forEach(function(d){
            paintPixel(ctx, d._source.doc.x_coordinate, d._source.doc.y_coordinate, colors[d._source.doc.color]);
        });
        start += 61;
        setTimeout(nextSecond,1);

    })
    .catch(function (error) {
        console.log(error);
    });
}

setTimeout(nextSecond,1);
