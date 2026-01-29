# Token Rent Back - Profile Validation API

> [!IMPORTANT]
> 🚧 **Work In Progress**: This project is currently being built up. Features and APIs are subject to change.

A minimal FastAPI service designed to validate user profiles by cross-referencing text input with data extracted from documents (ID Cards and Salary Slips) using Vision-Language Models (Qwen2-VL).

## Features
- **Profile Management**: Retrieve and validate user profile data.
- **AI-Powered OCR**: Uses `Qwen2-VL` via **Ollama** to verify documents locally.
- **Cross-Validation**: Automatically compares declared information (Name, Date of Birth, Salary) with document data.
- **Database**: MySQL integration for persistent profile storage.

## Tech Stack
- **Framework**: FastAPI (Python)
- **Framework**: FastAPI (Python)
- **AI/ML**: Ollama (running `qwen2-vl`), Requests
- **Database**: MySQL (via `mysql-connector-python`)
- **Validation**: Pydantic
- **Testing**: Pytest

## Getting Started

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com/) installed and running
- MySQL Server installed and running

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AntoineSierzputowski/token-rent-back.git
   cd token-rent-back
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup Environment**
   Create a `.env` file in the root directory:
   ```env
   DB_HOST=127.0.0.1
   DB_USER=root
   DB_PASSWORD=yourpassword
   DB_NAME=token_rent_back
   OLLAMA_URL=http://localhost:11434/api/generate
   OLLAMA_MODEL=qwen2-vl
   ```

4. **Prepare AI Model**
   ```bash
   ollama pull qwen2-vl
   ```

5. **Run the server**
   ```bash
   uvicorn server:app --reload
   ```

## Usage

### Validate a Profile
Send a `POST` request to `/create-profile` with the user's details and base64-encoded images of their ID and Salary Slip.

```json
{
  "profile_data": {
    "last_name": "Doe",
    "first_name": "John",
    "date_of_birth": "1990-01-01",
    "salary": 5000.0
  },
  "image1": "<base64_id_card>",
  "image2": "<base64_salary_slip>"
}
```

## Roadmap
- [x] Database integration (MySQL)
- [ ] Authentication & Authorization
- [ ] Enhanced error handling and logging
- [ ] Docker support
