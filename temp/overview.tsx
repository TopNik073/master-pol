"use client"

import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip } from "recharts"

const data = [
  {
    name: "1 Июн",
    total: 120000,
  },
  {
    name: "5 Июн",
    total: 240000,
  },
  {
    name: "10 Июн",
    total: 180000,
  },
  {
    name: "15 Июн",
    total: 350000,
  },
  {
    name: "20 Июн",
    total: 290000,
  },
  {
    name: "25 Июн",
    total: 410000,
  },
  {
    name: "30 Июн",
    total: 380000,
  },
]

export function Overview() {
  return (
    <ResponsiveContainer width="100%" height={350}>
      <BarChart data={data}>
        <XAxis dataKey="name" stroke="#888888" fontSize={12} tickLine={false} axisLine={false} />
        <YAxis
          stroke="#888888"
          fontSize={12}
          tickLine={false}
          axisLine={false}
          tickFormatter={(value) => `${value / 1000}k`}
        />
        <Tooltip
          formatter={(value: number) =>
            new Intl.NumberFormat("ru-RU", {
              style: "currency",
              currency: "RUB",
            }).format(value)
          }
        />
        <Bar dataKey="total" fill="#67ba80" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  )
}
