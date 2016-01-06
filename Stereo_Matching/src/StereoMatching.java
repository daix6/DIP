import java.awt.image.BufferedImage;

public class StereoMatching {
  public BufferedImage left, right;
  public BufferedImage disp_l, disp_r;
  public int max_d, patch;
  private double[] badRate;

  public StereoMatching(BufferedImage left, BufferedImage right) {
    this(left, right, 79, 5);
  }

  public StereoMatching(BufferedImage left, BufferedImage right, int max_disparity, int patch) {
    this.left = left;
    this.right = right;
    this.max_d = max_disparity;
    this.patch = patch;
  }

  public void caculateDisparity(MatchingCost mc) {
    double[][] left = Utils.getIntensity(this.left),
            right = Utils.getIntensity(this.right);
    
    int M = left.length, N = left[0].length; // M-Height, N-Width

    this.disp_l = new BufferedImage(N, M, BufferedImage.TYPE_BYTE_GRAY);
    this.disp_r = new BufferedImage(N, M, BufferedImage.TYPE_BYTE_GRAY);

    int[] ld = new int[M*N], rd = new int[M*N];
    
    for (int i = 0; i < M; i++) {
      for (int j = 0; j < N; j++) {
        double[][] lp = getPatch(left, i, j),
                   rp = getPatch(right, i, j);

        // For left eye image disparity map
        double cost = Double.POSITIVE_INFINITY;
        int min_d = 0;
        for (int d = 0; d < this.max_d; d++) {
          double[][] rp_d = getPatch(right, i, j - d);
          double matchingCost = mc.matchingCost(lp, rp_d);
          if (matchingCost < cost) {
            cost = matchingCost;
            min_d = d;
          }
        }
        ld[i*N + j] = min_d;

        // For right eye image disparity map
        cost = Double.POSITIVE_INFINITY;
        min_d = 0;
        for (int d = 0; d < this.max_d; d++) {
          double[][] lp_d = getPatch(left, i, j + d);
          double matchingCost = mc.matchingCost(rp, lp_d);
          if (matchingCost < cost) {
            cost = matchingCost;
            min_d = d;
          }
        }
        rd[i*N + j] = min_d;
      }
    }

    this.disp_l.getRaster().setPixels(0, 0, N, M, ld);
    this.disp_r.getRaster().setPixels(0, 0, N, M, rd);
  }

  public void caculateDisparityCIELab(MatchingCost mc) {
    int[][] left = Utils.getPixels(this.left),
            right = Utils.getPixels(this.right);
    int[][] leftLab = Utils.rgb2lab(left),
            rightLab = Utils.rgb2lab(right);
    
    int M = left.length, N = left[0].length;

    this.disp_l = new BufferedImage(N, M, BufferedImage.TYPE_BYTE_GRAY);
    this.disp_r = new BufferedImage(N, M, BufferedImage.TYPE_BYTE_GRAY);

    int[] ld = new int[M*N], rd = new int[M*N];

    for (int i = 0; i < M; i++) {
      for (int j = 0; j < N; j++) {
        int[][] lp = getPatch(left, i, j),
                rp = getPatch(right, i, j);

        int[][] lpLab = getPatch(leftLab, i, j),
                rpLab = getPatch(rightLab, i, j);

          // For left eye image disparity map
        double cost = Double.POSITIVE_INFINITY;
        int min_d = 0;
        for (int d = 0; d < this.max_d; d++) {
          int[][] rp_d = getPatch(right, i, j - d),
                  rpLab_d = getPatch(right, i, j - d);
          double matchingCost = mc.matchingCostLab(lp, rp_d, lpLab, rpLab_d);
          if (matchingCost < cost) {
              cost = matchingCost;
              min_d = d;
          }
        }
        ld[i*N + j] = min_d;

        // For right eye image disparity map
        cost = Double.POSITIVE_INFINITY;
        min_d = 0;
        for (int d = 0; d < this.max_d; d++) {
          int[][] lp_d = getPatch(left, i, j + d),
                  lpLab_d = getPatch(left, i, j + d);
          double matchingCost = mc.matchingCostLab(rp, lp_d, rpLab, lpLab_d);
          if (matchingCost < cost) {
            cost = matchingCost;
            min_d = d;
          }
        }
        rd[i*N + j] = min_d; 
      }
    }

    this.disp_l.getRaster().setPixels(0, 0, N, M, ld);
    this.disp_r.getRaster().setPixels(0, 0, N, M, rd);
  }
  
  // Helper
  public void evaluate(BufferedImage benchmark_left, BufferedImage benchmark_right) {
    try {
      if (this.disp_l.getType() != BufferedImage.TYPE_BYTE_GRAY || this.disp_r.getType() != BufferedImage.TYPE_BYTE_GRAY) {
        throw new Exception("Wrong image type.");
      }

      double[][] l = Utils.getIntensity(this.disp_l), r = Utils.getIntensity(this.disp_r);
      double[][] bpL = Utils.getIntensity(benchmark_left), bpR = Utils.getIntensity(benchmark_right);

      int M = benchmark_left.getHeight(), N = benchmark_right.getWidth();

      int[] bad= new int[] {0,0};
      for (int i = 0; i < M; i++) {
        for (int j = 0; j < N; j++) {
          if (Math.abs(l[i][j] - bpL[i][j] / 3.) > 1.)
            bad[0]++;
          if (Math.abs(r[i][j] - bpR[i][j] / 3.) > 1.)
            bad[1]++;
        }
      }

      this.badRate = new double[]{((float)bad[0]) / (M * N), ((float)bad[1]) / (M * N)};
    } catch(Exception e) {
      e.printStackTrace();
    }
  }

  public void printBad(String testcase, String method) {
    System.out.println("The percentage of bad pixels in case - " + testcase + ", with method: " + method);
    System.out.print(this.badRate[0]);
    System.out.print(" ");
    System.out.println(this.badRate[1]);
  }

  private double[][] getPatch(double[][] intensity, int x, int y) {
    double[][] patch = new double[this.patch][this.patch];
    int M = intensity.length, N = intensity[0].length;
    int pad = this.patch / 2;

    for (int i = x - pad; i < x + pad + 1; i++) {
      for (int j = y - pad; j < y + pad + 1; j++) {
        if (i >= 0 && j >= 0 && i < M && j < N)
          patch[i - x + pad][j - y + pad] = intensity[i][j];
        else
          patch[i - x + pad][j - y + pad] = 0;
      }
    }
    return patch;
  }
  
  private int[][] getPatch(int[][] pixels, int x, int y) {
      int[][] patch = new int[this.patch][this.patch];
      int M = pixels.length, N = pixels[0].length;
      int pad = this.patch / 2;

      for (int i = x - pad; i < x + pad + 1; i++) {
        for (int j = y - pad; j < y + pad + 1; j++) {
          if (i >= 0 && j >= 0 && i < M && j < N)
            patch[i - x + pad][j - y + pad] = pixels[i][j];
          else
            patch[i - x + pad][j - y + pad] = 0;
        }
      }
      return patch;
    }
}
