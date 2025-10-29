#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF页面提取工具
可以从PDF文件中提取指定页面范围并保存为新的PDF文件。
同时，为每个提取的PDF创建一个同名的空Markdown文件。
"""

import os
from pypdf import PdfReader, PdfWriter


def extract_pages(pdf_path, page_ranges, offset=0):
    """
    从PDF文件中提取指定页面范围，保存为新PDF，并创建同名Markdown文件。

    参数:
    pdf_path (str): PDF文件路径
    page_ranges (list): 页面范围列表，每个元素为(start, end, pdfname)元组，
                       表示从start到end的页面范围（包含两端）和输出PDF文件名
                       页面编号从1开始
    offset (int): 页面偏移量，默认为0。如果不为0，则在提取页面时会在start和end都加上这个偏移量

    输出:
    在原始PDF相同目录下创建指定名称的PDF文件和空的Markdown文件。

    异常:
    FileNotFoundError: 当PDF文件不存在时
    Exception: 当处理PDF文件出现其他错误时
    """
    # 检查PDF文件是否存在
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")

    try:
        # 获取PDF文件所在目录
        pdf_dir = os.path.dirname(pdf_path)
        if not pdf_dir:
            pdf_dir = "."

        # 读取PDF文件
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)

        print(f"PDF文件总页数: {total_pages}")

        # 处理每个页面范围
        for start, end, base_filename in page_ranges:
            # 应用页面偏移
            actual_start = start + offset
            actual_end = end + offset

            # 检查页面范围是否有效
            if actual_start < 1 or actual_end < 1:
                print(f"警告: 页面范围({start}, {end})加上偏移量{offset}后无效，页面编号应从1开始")
                continue

            if actual_start > total_pages or actual_end > total_pages:
                print(f"警告: 页面范围({start}, {end})加上偏移量{offset}后超出PDF总页数({total_pages})")
                continue

            if actual_start > actual_end:
                print(f"警告: 页面范围({start}, {end})加上偏移量{offset}后起始页大于结束页")
                continue

            # 创建PdfWriter对象
            writer = PdfWriter()

            # 添加指定范围的页面
            for page_num in range(actual_start - 1, actual_end):  # pypdf的页面索引从0开始
                writer.add_page(reader.pages[page_num])

            # --- PDF 文件处理 ---
            # 如果没有后缀自动加.pdf
            pdf_output_filename = base_filename
            if not pdf_output_filename.endswith(".pdf"):
                pdf_output_filename += ".pdf"

            # 生成PDF输出文件路径
            output_path = os.path.join(pdf_dir, pdf_output_filename)

            # 保存新的PDF文件
            with open(output_path, "wb") as output_file:
                writer.write(output_file)

            print(f"已保存页面范围 {start}-{end} 到文件: {output_path}")

            # --- Markdown 文件处理 ---
            # 使用基础文件名创建Markdown文件名
            md_output_filename = base_filename + ".md"
            md_output_path = os.path.join(pdf_dir, md_output_filename)

            # 创建空的Markdown文件
            try:
                with open(md_output_path, "w", encoding="utf-8") as md_file:
                    pass  # 创建并立即关闭文件，使其为空
                print(f"已创建Markdown文件: {md_output_path}")
            except Exception as e:
                print(f"创建Markdown文件 '{md_output_path}' 时出错: {e}")


    except Exception as e:
        print(f"处理PDF文件时出错: {e}")
        raise


def main():
    """
    主函数，直接设置PDF路径和提取列表
    """
    # 设置PDF文件路径
    pdf_path = "D:\\01学期课程2_2\\3_1\\编译原理\\Compilers.pdf"

    # 设置页面范围列表，格式为(start, end, pdfname)
    page_ranges = [
        (46, 98, "Chapter 1. Introduction"),
        (99, 189, "Chapter 2. A Simple Syntax-Directed Translator"),
        (190, 296, "Chapter 3. Lexical Analysis"),
        (297, 445, "Chapter 4. Syntax Analysis"),
        (446, 515, "Chapter 5. Syntax-Directed Translation"),
        (516, 611, "Chapter 6. Intermediate-Code Generation"),
        (612, 714, "Chapter 7. Run-Time Environments"),
        (715, 819, "Chapter 8. Code Generation"),
        (820, 982, "Chapter 9. Machine-Independent Optimizations"),
        (983, 1062, "Chapter 10. Instruction-Level Parallelism"),
        (1063, 1236, "Chapter 11. Optimizing for Parallelism and Locality"),
        (1237,  1350, "Chapter 12. Interprocedural Analysis"),
    ]

    try:
        extract_pages(pdf_path, page_ranges, offset=0)
        print("\n页面提取完成!")
    except FileNotFoundError:
        print(f"错误: 找不到PDF文件 '{pdf_path}'")
    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    main()