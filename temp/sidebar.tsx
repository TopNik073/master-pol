"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import { Building2, Users, ShoppingBag, Package, LayoutDashboard, Settings, LogOut } from "lucide-react"

const navItems = [
  {
    title: "Панель управления",
    href: "/admin",
    icon: LayoutDashboard,
  },
  {
    title: "Пользователи",
    href: "/admin/users",
    icon: Users,
  },
  {
    title: "Партнёры",
    href: "/admin/partners",
    icon: Building2,
  },
  {
    title: "Продажи",
    href: "/admin/sales",
    icon: ShoppingBag,
  },
  {
    title: "Типы продукции",
    href: "/admin/products",
    icon: Package,
  },
]

export function Sidebar() {
  const pathname = usePathname()

  return (
    <div className="hidden md:flex flex-col w-64 bg-67ba80 text-white">
      <div className="p-6">
        <div className="flex items-center space-x-2">
          <Building2 className="h-6 w-6" />
          <span className="text-xl font-bold">Мастер Пол</span>
        </div>
        <div className="text-sm opacity-70">Панель администратора</div>
      </div>
      <div className="flex-1 px-3 py-2">
        <nav className="space-y-1">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors",
                pathname === item.href
                  ? "bg-white bg-opacity-20 text-white"
                  : "text-white text-opacity-80 hover:bg-white hover:bg-opacity-10 hover:text-white",
              )}
            >
              <item.icon className="mr-3 h-5 w-5" />
              {item.title}
            </Link>
          ))}
        </nav>
      </div>
      <div className="p-4 border-t border-white border-opacity-20">
        <div className="flex items-center space-x-3 mb-3">
          <div className="w-10 h-10 rounded-full bg-white bg-opacity-20 flex items-center justify-center">
            <span className="font-medium text-sm">АА</span>
          </div>
          <div>
            <div className="font-medium">Админ Админов</div>
            <div className="text-xs opacity-70">admin@masterpol.ru</div>
          </div>
        </div>
        <div className="space-y-1">
          <Link
            href="/admin/settings"
            className="flex items-center px-3 py-2 rounded-md text-sm font-medium text-white text-opacity-80 hover:bg-white hover:bg-opacity-10 hover:text-white transition-colors"
          >
            <Settings className="mr-3 h-4 w-4" />
            Настройки
          </Link>
          <button className="w-full flex items-center px-3 py-2 rounded-md text-sm font-medium text-white text-opacity-80 hover:bg-white hover:bg-opacity-10 hover:text-white transition-colors">
            <LogOut className="mr-3 h-4 w-4" />
            Выйти
          </button>
        </div>
      </div>
    </div>
  )
}
