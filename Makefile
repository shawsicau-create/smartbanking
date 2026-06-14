# 智慧银行实验教程 Makefile
# 简化LaTeX编译流程

# 变量定义
MAIN = 智慧银行实验教程
CHAPTERS_DIR = 智慧银行实验教程chapters
PDF = $(CHAPTERS_DIR)/$(MAIN).pdf

# 默认目标
.PHONY: all
all: pdf

# 编译PDF
.PHONY: pdf
pdf:
	@echo "开始编译 $(MAIN).pdf..."
	cd $(CHAPTERS_DIR) && xelatex -interaction=nonstopmode "$(MAIN).tex"
	cd $(CHAPTERS_DIR) && biber "$(MAIN)"
	cd $(CHAPTERS_DIR) && xelatex -interaction=nonstopmode "$(MAIN).tex"
	cd $(CHAPTERS_DIR) && xelatex -interaction=nonstopmode "$(MAIN).tex"
	@echo "编译完成: $(PDF)"

# 清理编译文件
.PHONY: clean
clean:
	@echo "清理编译中间文件..."
	cd $(CHAPTERS_DIR) && rm -f *.aux *.log *.out *.toc *.bbl *.blg *.bcf *.run.xml *.synctex.gz *.fls *.fdb_latexmk *.nav *.snm *.vrb
	@echo "清理完成"

# 完全清理（包括PDF）
.PHONY: distclean
distclean: clean
	@echo "删除PDF文件..."
	cd $(CHAPTERS_DIR) && rm -f "$(MAIN).pdf"
	@echo "完全清理完成"

# 查看PDF
.PHONY: view
view: pdf
	@echo "打开PDF文件..."
	open "$(PDF)"

# 检查LaTeX语法（快速检查，不生成PDF）
.PHONY: check
check:
	@echo "检查LaTeX语法..."
	cd $(CHAPTERS_DIR) && xelatex -interaction=nonstopmode -no-pdf "$(MAIN).tex"
	@echo "语法检查完成"

# 统计字数
.PHONY: wordcount
wordcount:
	@echo "统计LaTeX文件字数..."
	@find $(CHAPTERS_DIR) -name "*.tex" -exec cat {} + | wc -w
	@echo "字数统计完成"

# 帮助信息
.PHONY: help
help:
	@echo "智慧银行实验教程 Makefile"
	@echo ""
	@echo "可用命令:"
	@echo "  make pdf       - 编译PDF文件"
	@echo "  make clean     - 清理编译中间文件"
	@echo "  make distclean - 完全清理（包括PDF）"
	@echo "  make view      - 编译并打开PDF"
	@echo "  make check     - 检查LaTeX语法"
	@echo "  make wordcount - 统计字数"
	@echo "  make help      - 显示帮助信息"
