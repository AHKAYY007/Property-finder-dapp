# Property Finder DApp

A decentralized property marketplace built with Sui Move smart contracts, FastAPI backend, and Next.js frontend.

## Project Structure

```
property-finder-dapp/
├── backend/         # FastAPI backend server
├── frontend/        # Next.js frontend application
└── contracts/       # Sui Move smart contracts
```

## Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL
- Sui CLI
- IPFS node (or use a gateway service)

## Setup Instructions

### 1. Smart Contract Deployment

```bash
# Install Sui CLI if not already installed
cargo install --locked --git https://github.com/MystenLabs/sui.git --branch devnet sui

# Configure Sui client for devnet
sui client switch --env devnet

# Build and deploy smart contracts
cd contracts
sui client publish --gas-budget 100000000
```

After deployment, copy the package ID and update:
- `contracts/Move.toml` - Update `published-at` address
- Backend `.env` - Update `PACKAGE_ID`
- Frontend `.env` - Update `PACKAGE_ID`

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create and configure .env file
cp .env.example .env
```

Configure your backend `.env` file with:
```env
# Database Configuration
DATABASE_URL=postgresql://actual_user:actual_password@localhost:5432/property_finder

# JWT Configuration
SECRET_KEY=generate_a_secure_random_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# IPFS Configuration
IPFS_NODE_URL=http://localhost:5001  # Or your IPFS service URL

# Sui Network Configuration
SUI_NETWORK_URL=https://fullnode.devnet.sui.io:443
PACKAGE_ID=your_deployed_package_id_here

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:3000
```

```bash
# Initialize database
alembic upgrade head

# Start backend server
uvicorn app.main:app --reload
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create and configure .env file
cp .env.example .env
```

Configure your frontend `.env` file with:
```env
# API Configuration
API_URL=http://localhost:8000

# Smart Contract Configuration
NETWORK=devnet
PACKAGE_ID=your_deployed_package_id_here

# IPFS Configuration
IPFS_GATEWAY=https://ipfs.io/ipfs/

# Sui Network
SUI_NETWORK=devnet
```

```bash
# Start frontend development server
npm run dev
```

## Environment Variables Guide

### Backend (.env)

1. **Database Configuration**
   - `DATABASE_URL`: Your PostgreSQL connection string
   - Format: `postgresql://user:password@host:port/database_name`
   - Example: `postgresql://postgres:mysecretpassword@localhost:5432/property_finder`

2. **JWT Configuration**
   - `SECRET_KEY`: Generate a secure random key
   - Generate using Python:
     ```python
     import secrets
     print(secrets.token_hex(32))
     ```
   - `ALGORITHM`: Keep as "HS256"
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: Adjust based on security needs (30 is recommended)

3. **IPFS Configuration**
   - `IPFS_NODE_URL`: Your IPFS node URL
   - Local node: `http://localhost:5001`
   - Or use a service like Infura/Pinata

4. **Sui Network Configuration**
   - `SUI_NETWORK_URL`: Use appropriate network URL
     - Devnet: `https://fullnode.devnet.sui.io:443`
     - Testnet: `https://fullnode.testnet.sui.io:443`
   - `PACKAGE_ID`: Your deployed smart contract package ID

### Frontend (.env)

1. **API Configuration**
   - `API_URL`: Backend API URL
   - Development: `http://localhost:8000`
   - Production: Your deployed API URL

2. **Smart Contract Configuration**
   - `NETWORK`: Match with backend (devnet/testnet)
   - `PACKAGE_ID`: Same as backend PACKAGE_ID

3. **IPFS Configuration**
   - `IPFS_GATEWAY`: Public IPFS gateway
   - Default: `https://ipfs.io/ipfs/`
   - Alternative: `https://gateway.pinata.cloud/ipfs/`

## Security Considerations

1. Never commit `.env` files to Git
2. Keep different environment configurations for development/staging/production
3. Regularly rotate JWT secrets and API keys
4. Use strong passwords for database
5. Monitor smart contract events and transactions

## Deployment Checklist

1. [ ] Deploy smart contracts to desired network
2. [ ] Update all configuration files with deployed contract address
3. [ ] Set up production database
4. [ ] Configure IPFS solution (local node or service)
5. [ ] Set up proper environment variables for production
6. [ ] Enable CORS with appropriate origins
7. [ ] Set up SSL/TLS for API endpoints
8. [ ] Configure proper network endpoints (devnet/testnet/mainnet)

## Support

For issues and feature requests, please open an issue in the repository. 