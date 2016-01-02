import java.awt.image.BufferedImage;
import java.awt.image.DataBufferByte;
import java.io.File;

import javax.imageio.ImageIO;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;

public class Utils {
	static public final int LEFT = 0;
	static public final int RIGHT = 1;
	static public final int BENCHMARK_LEFT = 2;
	static public final int BENCHMARK_RIGHT = 3;
	static public final String LEFT_IMAGE = "view1.png";
	static public final String RIGHT_IMAGE = "view5.png";
	static public final String LEFT_BENCHMARK = "disp1.png";
	static public final String RIGHT_BENCHMARK = "disp5.png";
	
	public static CommandLine parser(String[] args) {
		Options opts = new Options();
		opts.addOption("case", true, "The testcase that you want to run with");
		opts.addOption("all", false, "Run all testcase or not.");
		
		CommandLineParser parser = new DefaultParser();
		CommandLine cmd = null;
		try {
		    cmd = parser.parse(opts, args);
		} catch( ParseException exp ) {
	        // oops, something went wrong
	        System.err.println( "Parsing failed.  Reason: " + exp.getMessage() );
	    }

		return cmd;
	}

	public static String getAssetsFolder() {
		File file = new File("");
		String parentDir = file.getAbsolutePath();
		String assetsDir = parentDir + File.separator + "assets";
		return assetsDir;
	}

	public static BufferedImage getImage(String testcase, int which) {
		String assetsFolder = getAssetsFolder(), filename;

		switch(which) {
		case LEFT:
			filename = LEFT_IMAGE;
			break;
		case RIGHT:
			filename = RIGHT_IMAGE;
			break;
		case BENCHMARK_LEFT:
			filename = LEFT_BENCHMARK;
			break;
		case BENCHMARK_RIGHT:
			filename = RIGHT_BENCHMARK;
			break;
		default:
			filename = "";
		}

		String path = assetsFolder + File.separator + testcase + File.separator + filename;
		System.out.println(path);
		File file = new File(path);
		BufferedImage img = null;
		
		try {
			img = ImageIO.read(file);
			int type = img.getType();
			
			if (type != BufferedImage.TYPE_3BYTE_BGR && type != BufferedImage.TYPE_BYTE_GRAY) {
    			throw new Exception("Wrong image type.");
			}
		} catch(Exception e) {
			e.printStackTrace();
		}
		
		return img;
	}
	
	public static int[][] getPixels(BufferedImage image) {
		int type = image.getType();
		int w = image.getWidth();
		int h = image.getHeight();
		byte[] data = ((DataBufferByte)image.getRaster().getDataBuffer()).getData();
		int[][] pixels = new int[h][w];
		
		if (type == BufferedImage.TYPE_3BYTE_BGR) {
			final int pLength = 3;
			for (int p = 0, row = 0, col = 0; p < data.length; p += pLength) {
				int rgb = 0;
				rgb += ((int) data[p] & 0xff);           // blue
				rgb += (((int) data[p+1] & 0xff) << 8);  // green
				rgb += (((int) data[p+2] & 0xff) << 16); // red
				pixels[row][col] = rgb;
				col++;
				if (col == w) {
					col = 0;
					row++;
				}
			}
		} else if (type == BufferedImage.TYPE_BYTE_GRAY) {
			for (int p = 0, row = 0, col = 0; p < data.length; p++) {
				pixels[row][col] = (int)data[p];
				col++;
				if (col == w) {
					col = 0;
					row++;
				}
			}
		}

		return pixels;
	}
}
