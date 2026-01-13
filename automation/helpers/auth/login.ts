import { Page } from '@playwright/test';

export async function login(
  page: Page,
  email: string,
  password: string | number
) {
  // pakai URL lengkap biar aman
  await page.goto('http://localhost:5000/login');

  await page.fill('input[name="email"]', String(email));
  await page.fill('input[name="password"]', String(password));

  await page.click('button[type="submit"]');

  // tunggu navigasi / request selesai
  await page.waitForLoadState('networkidle');
}
