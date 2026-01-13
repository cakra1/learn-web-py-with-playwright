import { Page } from '@playwright/test';
import { formatDateDMY } from './date';

export async function register(page: Page, row: any) {
  await page.goto('http://localhost:5000/index-peserta');

  await page.fill('input[name="nama_lengkap"]', row.nama_lengkap);
  await page.fill('input[name="tempat_lahir"]', row.tempat_lahir);

  // 🔥 FIX DI SINI
  await page.fill(
    'input[name="tanggal_lahir"]',
    formatDateDMY(row.tanggal_lahir)
  );

  await page.click(`input[value="${row.gender}"]`);
  await page.fill('input[name="email"]', row.email);
  await page.fill('input[name="nomor_hp"]', row.nomor_hp);
  await page.fill('input[name="provinsi"]', row.provinsi);
  await page.fill('input[name="kota"]', row.kota);
  await page.fill('input[name="kecamatan"]', row.kecamatan);
  await page.fill('input[name="kelurahan"]', row.kelurahan);
  await page.fill('input[name="kode_pos"]', row.kode_pos);
  await page.fill('input[name="status_pernikahan"]', row.status_pernikahan);
  await page.fill('textarea[name="alamat_lengkap"]', row.alamat_lengkap);

  await page.click('button[type="submit"]');
}
