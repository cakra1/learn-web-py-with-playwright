import { Page } from '@playwright/test';
export async function signup(page: Page, row: any) {
  await page.goto('http://localhost:5000/register');

  await page.fill('input[name="name"]', row.Name.trim());
  await page.fill('input[name="email"]', row.Email.trim());
  await page.fill('input[name="password"]', row.Password.trim());
  await page.fill(
    'input[name="confirm_password"]',
    row['Confirm Password'].trim()
  );

  await page.click('button:has-text("SIGNUP")');
}
