# GitHub Pages 配置指南

本指南将帮助你启用 GitHub Pages，让仪表盘可以在线访问。

## 一、在 GitHub 仓库中启用 Pages

### 步骤 1：进入仓库设置

1. 打开你的 GitHub 仓库：https://github.com/Philbenzy/cftc-cot-report
2. 点击顶部导航栏的 **Settings（设置）**

### 步骤 2：配置 Pages

1. 在左侧边栏找到 **Pages** 选项
2. 在 **Source（来源）** 部分：
   - 选择 **GitHub Actions**（推荐）

   或者如果没有 GitHub Actions 选项：
   - 选择 **Deploy from a branch**
   - Branch 选择 **main**
   - 目录选择 **/ (root)**
   - 点击 **Save**

### 步骤 3：等待部署

- 配置完成后，GitHub 会自动开始部署
- 部署过程通常需要 1-3 分钟
- 你可以在仓库的 **Actions** 标签页查看部署进度

### 步骤 4：访问你的站点

部署完成后，你的仪表盘将可以通过以下地址访问：

**https://philbenzy.github.io/cftc-cot-report/dashboard.html**

## 二、自动部署说明

项目已配置两个 GitHub Actions 工作流：

### 1. `update-cot-data.yml` - 数据自动更新
- **触发时间**：每周五 23:00 UTC
- **功能**：自动获取最新 CFTC 数据并推送到仓库
- **文件**：`.github/workflows/update-cot-data.yml`

### 2. `deploy-pages.yml` - 自动部署到 Pages
- **触发条件**：每次推送到 main 分支
- **功能**：自动部署最新代码到 GitHub Pages
- **文件**：`.github/workflows/deploy-pages.yml`

## 三、数据加载机制

`dashboard.html` 使用三级数据加载回退机制：

1. **GitHub Raw CDN**（优先）
   - URL: `https://raw.githubusercontent.com/Philbenzy/cftc-cot-report/main/data/cot_data.json`
   - 优势：全球 CDN 加速，访问快速

2. **相对路径**（备用）
   - 路径：`./data/cot_data.json`
   - 适用于本地运行或 GitHub Pages

3. **内置数据**（兜底）
   - 内置在 HTML 中的样例数据
   - 确保即使网络问题也能查看界面

## 四、验证部署

部署完成后，你可以验证：

1. **访问在线仪表盘**：https://philbenzy.github.io/cftc-cot-report/dashboard.html
2. **检查数据加载**：打开浏览器开发者工具（F12）→ Console，查看是否有错误
3. **确认数据源**：在控制台中应该能看到成功从 GitHub Raw 加载数据的日志

## 五、常见问题

### Q1：部署后显示 404
- 确保 Pages 已在设置中启用
- 检查分支是否选择正确（main）
- 等待几分钟让 DNS 生效

### Q2：页面显示但数据加载失败
- 检查 `data/cot_data.json` 文件是否存在
- 确认数据更新 workflow 已成功运行
- 在浏览器控制台查看具体错误信息

### Q3：想要自定义域名
- 在 Pages 设置中可以配置 Custom domain
- 需要在你的域名提供商处添加 CNAME 记录

## 六、手动触发更新

如果需要立即更新数据（不等每周五自动运行）：

1. 进入仓库的 **Actions** 标签页
2. 点击左侧的 **Update COT Data** workflow
3. 点击右侧的 **Run workflow** 按钮
4. 选择 main 分支
5. 点击绿色的 **Run workflow** 按钮

数据更新后，deploy-pages workflow 会自动触发，重新部署站点。

---

配置完成后，你的 COT 数据仪表盘就可以在线访问了！🎉
