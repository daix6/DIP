var image = function() {
  var sample = new Image();
  sample.onload = function() {
  };
  sample.src = './sample.png';

  return sample;
}();

(function(w) {
  var init = function() {
  	if (image.complete) {
			var w = image.width;
			var h = image.height;

			var canvas = document.getElementById("pic");
			var context = canvas.getContext('2d');
			canvas.setAttribute('width', w);
			canvas.setAttribute('height', h);
			context.drawImage(image, 0, 0, w, h);

			var pixels = context.getImageData(0, 0, w, h).data;

			var pixels_ = [];
			for (var i = 0; i < h; i++) {
			  var row = [];
			  for (var j = 0; j < w*4; j += 4) {
			    var rgb = [];
			    rgb[0] = pixels[i*w*4+j];
			    rgb[1] = pixels[i*w*4+j+1];
			    rgb[2] = pixels[i*w*4+j+2];
			    rgb[3] = pixels[i*w*4+j+3];
			    row[j/4] = rgb;
			  }
			  pixels_[i] = row; 
			  }

			var newc = context.createImageData(w, h);
			var output = newc.data;

			for (var i = 0; i < h; i++) {
			  for (var j = 0; j < w*4; j += 4) {
			    var base = i*w*4+j;
			    output[base] = pixels_[i][j/4][0];
			    output[base+1] = 0;
			    output[base+2] = 0;
			    output[base+3] = pixels_[i][j/4][3];
			  }
			}
			context.putImageData(newc, 0, 0);
  	}
  }

  window.onload = function() {
    init();
  }

}(window));
