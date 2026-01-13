import { test, expect } from '@playwright/test';
import { login } from '../../helpers/auth/login';
import { readExcel } from '../../helpers/excel/readExcel';
import path from 'path';

type LoginData = {
  email: string;
  password: string;
  expected: string;
};

const data = readExcel(
  path.join(__dirname, '../../excel/login.xlsx')
) as LoginData[];

test.describe('Login Data Driven Test', () => {
  for (const row of data) {
    test(`login ${row.email} - ${row.expected}`, async ({ page }) => {
      await login(page, row.email, row.password);

      const expected = String(row.expected || '').trim().toLowerCase();

      if (expected === 'success') {
        // ✅ PALING BENAR: cek halaman admin / peserta
        await expect(page).toHaveURL(/admin|peserta/);
      } else if (expected === 'fail') {
        await expect(
          page.locator('.alert-danger')
        ).toBeVisible();
      } else {
        test.fail(
          true,
          `Expected value INVALID di Excel: ${row.expected}`
        );
      }
    });
  }
});
