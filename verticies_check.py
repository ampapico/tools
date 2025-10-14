import matplotlib.pyplot as plt

# 座標データ
points = [
    [
        0,
        0,
        0
    ],
    [
        0,
        5200,
        0
    ],
    [
        9200,
        5200,
        0
    ],
    [
        9200,
        -1000,
        0
    ],
    [
        5500,
        -1000,
        0
    ],
    [
        5500,
        0,
        0
    ],
    [
        0,
        0,
        0
    ]
]

# [
#     [
#         0,
#         0,
#         0
#     ],
#     [
#         0,
#         5000,
#         0
#     ],
#     [
#         9000,
#         5000,
#         0
#     ],
#     [
#         9000,
#         -1000,
#         0
#     ],
#     [
#         5500,
#         -1000,
#         0
#     ],
#     [
#         5500,
#         0,
#         0
#     ],
#     [
#         0,
#         0,
#         0
#     ]
# ]


# x, y 座標を抽出
x = [p[0] for p in points]
y = [p[1] for p in points]

# 図を描画
plt.figure(figsize=(8, 6))
plt.plot(x, y, marker='o', linestyle='-', color='b')
plt.axis('equal')  # 比率を1:1にする
plt.grid(True)
plt.title("2D Polygon Shape from Coordinates")
plt.xlabel("X")
plt.ylabel("Y")

# 座標をラベル表示（確認用）
for i, (xx, yy) in enumerate(zip(x, y)):
    plt.text(xx, yy, f"{i}", fontsize=8, color="red")

plt.show()
