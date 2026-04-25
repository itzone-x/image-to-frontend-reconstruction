# Image to Frontend Reconstruction

`image-to-frontend-reconstruction` 是一个面向 Codex/Claude 的 skill，用来把 UI 参考图、AI 生成的产品原型图、截图或设计稿，高保真地还原成前端页面。

它的核心思路很直接：不要让大模型凭感觉把整张图重新“画”一遍，而是先把参考图拆成三层：原生前端 UI、从原图提取的图片资产，以及低风险的 CSS 基础图形。文字、布局、按钮、输入框等内容用前端原生实现；复杂图标、装饰纹理、插画碎片、背景元素等容易走样的部分，则尽量从原始设计图中切出来使用。

## 为什么做这个 Skill

Stitch、Figma、GPT Image 这类工具，已经可以很快生成观感不错的产品设计稿。真正麻烦的地方通常出现在下一步：怎么把这张图变成真实可用的前端页面。

如果你不是前端开发，也没有专业 UI 设计师帮你切图，落地过程很容易卡住。即使交给大模型直接“看图写页面”，效果也经常会有偏差：模型能生成一个看起来相似的页面，但它不是在做真正的设计稿切图。图标细节、间距、背景纹理、按钮质感、卡片层次，都可能在实现时慢慢漂移。

这个 skill 固化了一套更接近真实 UI 切图和前端开发的流程：

- 先查看原图尺寸和真实像素，不凭缩略图猜测；
- 反推出颜色、字体层级、间距、圆角、阴影和卡片结构；
- 编码前先判断每个视觉元素应该原生实现、切图提取，还是用 CSS 简单绘制；
- 对复杂图标、背景装饰、纹理和插画碎片进行确定性的资产提取；
- 文字、控件和布局保持前端原生，方便后续改文案、加交互和做适配；
- 在多个真实设备宽度下检查效果，而不是只对齐一张截图。

作者在多种场景中试用后发现，这套方法在不少 To C 高保真原型上大约能达到 90% 左右的还原度；对于一些组件更规整的后台或管理系统页面，部分场景可以做到更接近原稿的复刻效果。

## 仓库结构

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   └── extract_reference_assets.py
├── docs/
│   └── wechat-article.md
├── requirements.txt
└── LICENSE
```

## 安装

Codex 用户可以复制到本地 skills 目录：

```bash
mkdir -p ~/.codex/skills/image-to-frontend-reconstruction
cp -R SKILL.md agents scripts ~/.codex/skills/image-to-frontend-reconstruction/
```

如果你使用 Claude Code 或 Claude Desktop 的 skill 机制，也可以把同样的文件复制到对应的 skill 目录中，当然其他大语言模型只要支持skill的都可以直接使用。

## 使用方式

当你需要根据一张视觉参考图实现页面时，可以这样要求你的 coding agent：

```text
  之后你只要在需求里明确提到它即可，例如：
  使用 image-to-frontend-reconstruction skill，基于 /path/to/reference.png 高保真还原问答页。

  或者更自然一点：
  请按这张 GPT Image2 视觉稿高保真还原页面，图标和背景装饰优先从原图裁切，不要手绘近似。

  它会触发的典型场景包括：
  - “根据这张图还原前端页面”
  - “把 GPT Image2 生成的视觉稿落成小程序或者你想要的页面”
  - “图标不要手绘，直接从参考图切图”
  - “从截图/设计稿提取背景装饰并实现页面”
  - “高保真还原 UI mockup”

  推荐你后续这样给这个skill任务，作者已多次验证效果：
  使用 image-to-frontend-reconstruction 和 frontend-design。
  参考图在 miniprogram/path/to/reference.png。（注意：这里是你存放参考图的地址，参考图一定要指定地址）
  目标页面是 miniprogram/pages/intake/。（注意：这里的目标页面指的是你要开发实现的页面，skill会根据参考图直接在这里生成你想要的高保真复刻页面）
  要求：保留现有业务逻辑和文案，按参考图高保真还原 UI；图标、背景纹理、装饰元素从参考图提取资产。

  skill就会按这个流程执行：读参考图 → 反推 UI 规范 → 判断哪些用原生 UI、哪些切图 → 生成 assets → 改 WXML/WXSS → 更新测试 → 跑验证。
```

仓库内附带了一个小工具，可以按坐标裁剪图片资产，也可以生成透明背景装饰层：

```bash
python3 scripts/extract_reference_assets.py \
  --source reference.png \
  --out-dir src/assets/home \
  --crop hero-icon=120,180,220,280 \
  --decor-output src/assets/home/background-decor.png \
  --mask 0,120,390,640
```

脚本依赖 Pillow：

```bash
pip install -r requirements.txt
```

## 它不是什么

它不是“上传截图，自动生成完美 App”的魔法按钮，而是一套约束大模型工作方式的流程。

它最适合这样的场景：你有原始参考图，目标前端项目可以引用本地图片资产，并且最终有人愿意做一轮视觉检查。字体渲染、平台控件差异、响应式适配、图片缩放方式等因素，仍然可能带来细微差异，需要人工判断和微调。

## License

MIT
