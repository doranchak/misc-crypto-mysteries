"""Robust fit of the two straight marks on the commemorative coin (crop assets/coin_front.jpg, 420x420)."""
import numpy as np, cv2, math
im = cv2.imread('../assets/coin_front.jpg', cv2.IMREAD_GRAYSCALE).astype(np.float32)
bg = cv2.medianBlur(im.astype(np.uint8), 31).astype(np.float32)
diff = bg - im                       # positive where darker than local background
H, W = im.shape
Y, X = np.mgrid[0:H, 0:W]
# coin face mask: inside radius ~175 of approx centre (210,210)
face = np.hypot(X - 210, Y - 205) < 178
mask = (diff > 25) & face
ys, xs = np.nonzero(mask)
print('dark pixels', len(xs))
pts = np.stack([xs, ys], 1).astype(float)
rng = np.random.default_rng(1)
def ransac(P, iters=4000, tol=2.5):
    best = None
    for _ in range(iters):
        a, b = P[rng.choice(len(P), 2, replace=False)]
        d = b - a; n = np.hypot(*d)
        if n < 40: continue
        d /= n; nrm = np.array([-d[1], d[0]])
        dist = np.abs((P - a) @ nrm)
        inl = dist < tol
        if best is None or inl.sum() > best.sum(): best = inl
    Q = P[best]; mu = Q.mean(0); _, _, vt = np.linalg.svd(Q - mu); d = vt[0]
    return mu, d, best
lines = []
P = pts.copy()
for k in range(2):
    mu, d, inl = ransac(P)
    Q = P[inl]
    # orient from the inner end to the tip (tip = far end from the hub circle ~ (197,203))
    proj = (Q - mu) @ d
    e1, e2 = mu + d * proj.min(), mu + d * proj.max()
    hub = np.array([197.3, 203.3])
    if np.hypot(*(e1 - hub)) > np.hypot(*(e2 - hub)): e1, e2 = e2, e1
    dd = (e2 - e1) / np.hypot(*(e2 - e1))
    bearing = math.degrees(math.atan2(dd[0], -dd[1])) % 360
    resid = np.abs((Q - mu) @ np.array([-d[1], d[0]]))
    print(f'line {k}: inliers {inl.sum()}, inner end {e1.round(1)}, tip {e2.round(1)}, bearing {bearing:.2f}, rms {np.sqrt((resid**2).mean()):.2f}px')
    lines.append((mu, dd, e1, e2, bearing))
    # remove this line's pixels (wider band) and continue
    far = np.abs((P - mu) @ np.array([-d[1], d[0]])) > 6
    P = P[far]
# intersection
(m1, d1, *_), (m2, d2, *_) = lines
A = np.array([d1, -d2]).T; t = np.linalg.solve(A, m2 - m1); vtx = m1 + d1 * t[0]
b = sorted(l[4] for l in lines)
print('vertex', vtx.round(1), 'bearings', [round(x, 2) for x in b], 'angle between', round(b[1] - b[0], 2))
np.save('coin_lines.npy', np.array([[*lines[i][2], *lines[i][3], lines[i][4]] for i in range(2)] + [[*vtx, 0, 0, 0]]))
