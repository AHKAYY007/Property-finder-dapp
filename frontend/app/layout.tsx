import { WalletKitProvider } from '@mysten/wallet-kit'
import { Toaster } from 'react-hot-toast'
import './globals.css'
import { Inter } from 'next/font/google'
import Navbar from '@/components/Navbar'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Property Finder DApp',
  description: 'A decentralized property listing and management platform built on Sui blockchain',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <WalletKitProvider>
          <Toaster position="top-right" />
          <div className="min-h-screen bg-gray-50">
            <Navbar />
            <main className="container mx-auto px-4 py-8">
              {children}
            </main>
          </div>
        </WalletKitProvider>
      </body>
    </html>
  )
} 