public class ASW implements MatchingCost {
  public double k, gammaC, gammaP;

  public ASW() {
    this.k = 1;
    this.gammaC = 45;
    this.gammaP = 5;
  }

  public ASW(double k, double gammaC, double gammaP) {
    this.k = k;
    this.gammaC = gammaC;
    this.gammaP = gammaP;
  }

  // It should not be used.
  public double matchingCost(double[][] left, double[][] right) { return 0; }

  public double matchingCostLab(int[][] left, int[][] right, int[][] leftLab, int[][] rightLab) {
    int M = left.length, N = left[0].length;
    int centerI = M / 2, centerJ = N / 2;

    double nominator = 0, denominator = 0;
    for (int i = 0; i < M; i++) {
      for (int j = 0; j < N; j++) {
        double wlwr = w(leftLab[centerI][centerJ], leftLab[i][j], centerI, centerJ, i, j)
                    * w(rightLab[centerI][centerJ], rightLab[i][j], centerI, centerJ, i, j);
        double e0 = e(left[i][j], right[i][j]);
        nominator += wlwr * e0;
        denominator += wlwr;
      }
    }

    return nominator / denominator;
  }

  private double w(int pLab, int qLab, int px, int py, int qx, int qy) {
    return this.k * Math.exp(-similarity(pLab, qLab) - proximity(px, py, qx, qy));
  }

  private double e(int pRGB, int pdRGB) {
    int pR = ((int)pRGB >> 16) & 0xff,
        pG = ((int)pRGB >> 8) & 0xff,
        pB = (int)pRGB & 0xff;

    int pdR = ((int)pdRGB >> 16) & 0xff,
        pdG = ((int)pdRGB >> 8) & 0xff,
        pdB = (int)pdRGB & 0xff;

    return Math.abs(pR - pdR) + Math.abs(pG - pdG) + Math.abs(pB - pdB);
  }

  private double similarity(int pLab, int qLab) {
    int pL = ((int)pLab >> 16) & 0xff,
        pA = ((int)pLab >> 8) & 0xff,
        pB = ((int)pLab) & 0xff;

    int qL = ((int)qLab >> 16) & 0xff,
        qA = ((int)qLab >> 8) & 0xff,
        qB = ((int)qLab) & 0xff;

    return Math.sqrt(Math.pow(pL-qL, 2) + Math.pow(pA-qA, 2) + Math.pow(pB-qB, 2)) / this.gammaC;
  }

  private double proximity(int px, int py, int qx, int qy) {
    return Math.sqrt(Math.pow(px - qx, 2) + Math.pow(py - qy, 2)) / this.gammaP;
  }
}
