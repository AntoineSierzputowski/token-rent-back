# Token Rent Back - Profile Validation API

> [!IMPORTANT]
> 🚧 **Work In Progress**: This project is currently being built up. Features and APIs are subject to change.

A minimal FastAPI service designed to validate user profiles by cross-referencing text input with data extracted from documents (ID Cards and Salary Slips) using Vision-Language Models (Qwen2-VL).

## Features
- **Profile Management**: Retrieve and validate user profile data.
- **AI-Powered OCR**: Uses `Qwen2-VL` to extract text from images.
- **Cross-Validation**: Automatically compares declared information (Name, Date of Birth, Salary) with document data.
- **Mock Database**: In-memory state management for rapid prototyping.

## Tech Stack
- **Framework**: FastAPI (Python)
- **AI/ML**: HuggingFace Transformers, Qwen2-VL
- **Validation**: Pydantic
- **Testing**: Pytest

## Getting Started

### Prerequisites
- Python 3.10+
- (Optional) CUDA-capable GPU for faster inference

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

3. **Run the server**
   ```bash
   uvicorn main:app --reload
   ```

## Usage

### Validate a Profile
Send a `POST` request to `/create-profile` with the user's details and base64-encoded images of their ID and Salary Slip.

```json
{
  "text_data": {
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
- [ ] Database integration (PostgreSQL)
- [ ] Authentication & Authorization
- [ ] Enhanced error handling and logging
- [ ] Docker support
