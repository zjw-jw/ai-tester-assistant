import asyncio
import os
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 加载 .env 文件
load_dotenv()


async def main():
    print("准备启动蓝湖 MCP Server...")

    # 读取环境变量
    my_lanhu_cookie = os.getenv("LANHU_COOKIE")
    my_prd_url = os.getenv("LANHU_PRD_URL")

    if not my_lanhu_cookie:
        print("❌ 错误：没有在 .env 中读取到 LANHU_COOKIE！")
        return
    if not my_prd_url:
        print("❌ 错误：没有在 .env 中读取到 LANHU_PRD_URL！")
        return

    print(f"✅ 成功读取 Cookie，长度: {len(my_lanhu_cookie)} 字符")
    print(f"✅ 目标 PRD 链接: {my_prd_url}")

    server_params = StdioServerParameters(
        command="npx.cmd",
        args=["-y", "mcp-lanhu"],
        env={
            **os.environ,
            "LANHU_COOKIE": my_lanhu_cookie,
        }
    )

    try:
        async with stdio_client(server_params) as (read, write):
            print("\n✅ 进程启动成功，正在初始化 MCP 协议...")

            async with ClientSession(read, write) as session:
                await session.initialize()
                print("✅ MCP 通信建立成功！")

                print(f"\n正在向 MCP 请求解析 PRD...")

                try:
                    # 调用工具，传入从环境变量读取的 URL
                    result = await session.call_tool(
                        "lanhu_page",
                        arguments={
                            "url": my_prd_url,
                            "mode": "list"  # <--- 把 analyze 改成 list
                        }
                    )

                    print("\n🎉 成功获取 PRD 数据：")
                    for content in result.content:
                        print(content.text)

                except Exception as e:
                    print(f"\n❌ 获取 PRD 失败，错误信息: {e}")

    except Exception as e:
        print(f"\n❌ 连接失败，错误信息: {e}")


if __name__ == "__main__":
    asyncio.run(main())