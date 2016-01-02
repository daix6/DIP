import java.awt.image.BufferedImage;

public class StereoMatching {
	public BufferedImage left, right;
	public BufferedImage disp_l, disp_r;
	public int max_d, patch;
	
	public StereoMatching(BufferedImage left, BufferedImage right) {
	    this(left, right, 79, 5);
	}
	
    public StereoMatching(BufferedImage left, BufferedImage right, int max_disparity, int patch) {
    	this.left = left;
    	this.right = right;
    	this.max_d = max_disparity;
    	this.patch = patch;
    }

    public double evaluate(BufferedImage test, BufferedImage benchmark) {
    	try {
    		if (test.getType() != BufferedImage.TYPE_BYTE_GRAY) {
    			throw new Exception("Wrong image type.");
    		}
    	
    		int[][] tp = Utils.getPixels(test);
    		int[][] bp = Utils.getPixels(benchmark);
    		
    		int bad = 0;
    		int h = test.getHeight();
    		int w = test.getWidth();
    		for (int i = 0; i < h; i++) {
    			for (int j = 0; j < h; j++) {
    				if (Math.abs(tp[i][j] - bp[i][j] / 3.0) > 1)
    					bad++;
    			}
    		}
 
    		return ((float)bad) / (w * h);
    	} catch(Exception e) {
    		e.printStackTrace();
    	}
    	return 0.0;
    }
}
