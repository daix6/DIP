# DIP Homework 4: Image Restoration and Color Image Processing1
## 戴旋, 13331043

## 1 Exercises

### 1.1 Color Spaces

1. HSI 模型优于 RGB 模型：对 HSI 模型来说，在进行空间域滤波的时候，我们可以单独对 Intensity 分量滤波。而对于 RGB 模型，需要分别对 RGB 三个分量进行滤波再整合。从这点上看 HSI 模型优于 RGB 模型。  
RGB 模型优于 HSI 模型：噪声对于 HSI 分量的影响很大，去噪很困难。而对于 RGB 分量，影响小得多，去噪处理也方便。

2. 如果 $ H \in [270, 360) $ 或 $ H \in [0, 60) $，给 H 加了 $ 60^{\circ} $ 后，颜色在 RG 扇形内。根据公式：
$$\begin{align\*}
B & = I(1 - S) \\\\
R & = I[1 + \frac{Scos(H + 60^{\circ})}{cosH}] \\\\
G & = 3I - (R + B)
\end{align\*}$$
如果 $ H \in [60, 180) $，给 H 加了 $ 60^{\circ} $ 后，颜色在 GB 扇形内。根据公式：
$$\begin{align\*}
R & = I(1 - S) \\\\
G & = I\[1 + \frac{Scos(H + 60^{\circ})}{cosH}\] \\\\
B & = 3I - (R + G)
\end{align\*}$$
如果 $ H \in [180, 270) $，给 H 加了 $ 60^{\circ} $ 后，颜色在 BR 扇形内。根据公式：
$$\begin{align\*}
G & = I(1 - S) \\\\
B & = I\[1 + \frac{Scos(H + 60^{\circ})}{cosH}\] \\\\
R & = 3I - (G + B)
\end{align\*}$$

### 1,2 Color composition

<center>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 110 110" width="220" height="220"><line x1="10" y1="0" x2="10" y2="110" stroke="black"></line><line x1="0" y1="100" x2="110" y2="100" stroke="black"></line><polygon points="20,90 40,5 95,70" fill="white" stroke="black"></polygon><circle cx="50" cy="50" r="1" stroke-width="0" fill="black"></circle><line x1="50" y1="50" x2="57" y2="80" stroke="black" stroke-dasharray="1,1"></line><text x="20" y="95" font-size="8px" font-style="italic">c1(x1,y1)</text><text x="50" y="10" font-size="8px" font-style="italic">c2(x2,y2)</text><text x="75" y="85" font-size="8px" font-style="italic">c3(x3,y3)</text><text x="50" y="60" font-size="8px" font-style="italic">c0(x0,y0)</text><text x="55" y="90" font-size="8px" font-style="italic">d(a,b)</text></svg>
</center>

设 $c_0(x_0,y_0)$为 $c_1,c_2,c_3$ 围成的三角形中的任意一点（一种颜色），作 $c_{0}d \perp c_1c_3$ 交 $c_1c_3$ 于 $d(a,b)$， 如上图所示。  
$p_1,p_2,p_3$ 为 $c_0$ 中 $c_1,c_2,c_3$ 的百分比，设 $dis(p_a,p_b)=\sqrt{(x_a-x_b)^2 + (y_a-y_b)^2}$ 有：
$$\begin{align\*}
p_1 & = \frac{dis(c_1, c_3) - dis(d,c_3)}{dis(c_1,c_3)} \\\\
p_3 & = \frac{dis(c_1, c_3) - dis(d,c_1)}{dis(c_1,c_3)} \\\\
100 & = p_1 + p_2 + p_3
\end{align\*}$$
通过上式即能得出组成给定颜色 $c_0$ 中 $c_1,c_2,c_3$ 的百分比 $p_1,p_2,p_3$。

## 2 Programming Tasks

### 2.1 Image Filtering

#### 2.1.1 Result

#### 2.1.2 Discussion

#### 2.1.3 Algorithm