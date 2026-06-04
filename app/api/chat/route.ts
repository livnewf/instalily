import { NextRequest, NextResponse } from 'next/server';

const PYTHON_BACKEND_URL = process.env.PYTHON_BACKEND_URL ?? 'http://localhost:8000/chat';

async function parseBackendError(response: Response) {
  const text = await response.text();
  try {
    return JSON.parse(text);
  } catch {
    return { error: text || 'Unknown backend error' };
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const response = await fetch(PYTHON_BACKEND_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const backendError = await parseBackendError(response);
      return NextResponse.json(
        {
          reply: 'Unable to process the request. The backend returned an error.',
          error: backendError,
          products: [],
        },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    return NextResponse.json(
      {
        reply: 'Unable to process the request. The backend could not be reached.',
        error: String(error),
        products: [],
      },
      { status: 500 }
    );
  }
}
