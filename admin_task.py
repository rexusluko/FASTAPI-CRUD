import asyncio
from datetime import timedelta

import httpx
import openpyxl
from celery import Celery

base_url = 'http://web:8000/api/v1'
delete_row = 0


loop = asyncio.get_event_loop()
semaphore = asyncio.Semaphore(1)


async def create_menu(create_data: dict) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(f'{base_url}/menus', json=create_data)
        return response.json()['id']


async def update_menu(menu_id: str, update_data: dict) -> None:
    async with httpx.AsyncClient() as client:
        url = f'{base_url}/menus/{menu_id}'
        response = await client.get(url=url)
        current_menu = response.json()
        if current_menu['title'] != update_data['title'] or current_menu['description'] != update_data['description']:
            await client.patch(url=url, json=update_data)


async def delete_menu(menu_id: str) -> None:
    async with httpx.AsyncClient() as client:
        await client.delete(f'{base_url}/menus/{menu_id}')


async def create_submenu(menu_id: str, create_data: dict) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(f'{base_url}/menus/{menu_id}/submenus', json=create_data)
        return response.json()['id']


async def update_submenu(menu_id: str, submenu_id: str, update_data: dict) -> None:
    async with httpx.AsyncClient() as client:
        url = f'{base_url}/menus/{menu_id}/submenus/{submenu_id}'
        response = await client.get(url=url)
        current_submenu = response.json()
        if current_submenu['title'] != update_data['title'] or current_submenu['description'] != update_data[
                'description']:
            await client.patch(url=url, json=update_data)


async def delete_submenu(menu_id: str, submenu_id: str) -> None:
    async with httpx.AsyncClient() as client:
        await client.delete(f'{base_url}/menus/{menu_id}/submenus/{submenu_id}')


async def create_dish(menu_id: str, submenu_id: str, create_data: dict) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(f'{base_url}/menus/{menu_id}/submenus/{submenu_id}/dishes', json=create_data)
        return response.json()['id']


async def update_dish(menu_id: str, submenu_id: str, dish_id: str, update_data: dict) -> None:
    async with httpx.AsyncClient() as client:
        url = f'{base_url}/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
        response = await client.get(url=url)
        current_dish = response.json()
        if current_dish['title'] != update_data['title'] or current_dish['description'] != update_data['description'] or \
                current_dish['price'] != update_data['price']:
            await client.patch(url=url, json=update_data)


async def delete_dish(menu_id: str, submenu_id: str, dish_id: str) -> None:
    async with httpx.AsyncClient() as client:
        await client.delete(f'{base_url}/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')


async def create_and_update_from_excel(filepath: str) -> None:
    global delete_row
    menu_id_column, menu_title_column, menu_description_column = 1, 2, 3
    submenu_id_column, submenu_title_column, submenu_description_column = 2, 3, 4
    dish_id_column, dish_title_column, dish_description_column, dish_price_column = 3, 4, 5, 6
    wb = openpyxl.load_workbook(filepath)
    sheet = wb.active
    row = 1
    while sheet.cell(row=row, column=menu_description_column).value and (
            sheet.cell(row=row, column=submenu_description_column).value is None):  # цикл по меню
        menu_title = sheet.cell(row=row, column=menu_title_column).value
        menu_description = sheet.cell(row=row, column=menu_description_column).value
        menu_data = {'title': menu_title, 'description': menu_description}
        if sheet.cell(row=row, column=menu_id_column).value:
            menu_id = sheet.cell(row=row, column=menu_id_column).value
            async with semaphore:
                await update_menu(menu_id, menu_data)
        else:
            async with semaphore:
                menu_id = await create_menu(menu_data)
            sheet.cell(row=row, column=menu_id_column).value = menu_id
        row += 1
        while sheet.cell(row=row, column=submenu_description_column).value and (
                sheet.cell(row=row, column=dish_description_column).value is None):  # цикл по подменю
            submenu_title = sheet.cell(row=row, column=submenu_title_column).value
            submenu_description = sheet.cell(row=row, column=submenu_description_column).value
            submenu_data = {'title': submenu_title, 'description': submenu_description}
            if sheet.cell(row=row, column=submenu_id_column).value:
                submenu_id = sheet.cell(row=row, column=submenu_id_column).value
                async with semaphore:
                    await update_submenu(menu_id, submenu_id, submenu_data)
            else:
                async with semaphore:
                    submenu_id = await create_submenu(menu_id, submenu_data)
                sheet.cell(row=row, column=submenu_id_column).value = submenu_id
            row += 1
            while sheet.cell(row=row, column=dish_description_column).value:  # цикл по блюдам
                dish_title = sheet.cell(row=row, column=dish_title_column).value
                dish_description = sheet.cell(row=row, column=dish_description_column).value
                dish_price = str(sheet.cell(row=row, column=dish_price_column).value)
                dish_data = {'title': dish_title, 'description': dish_description, 'price': dish_price}
                if sheet.cell(row=row, column=dish_id_column).value:
                    dish_id = sheet.cell(row=row, column=dish_id_column).value
                    async with semaphore:
                        await update_dish(menu_id, submenu_id, dish_id, dish_data)
                else:
                    async with semaphore:
                        dish_id = await create_dish(menu_id, submenu_id, dish_data)
                    sheet.cell(row=row, column=dish_id_column).value = dish_id
                row += 1
    wb.save(filepath)
    wb.close()
    delete_row = row + 3


async def delete_from_excel(filepath: str, start_row: int) -> None:
    menu_menu_id = 1
    submenu_menu_id, submenu_submenu_id = 3, 4
    dish_menu_id, dish_submenu_id, dish_dish_id = 6, 7, 8
    wb = openpyxl.load_workbook(filepath)
    sheet = wb.active
    row = start_row
    while sheet.cell(row=row, column=menu_menu_id).value:  # цикл для удаления меню
        menu_id = sheet.cell(row=row, column=menu_menu_id).value
        async with semaphore:
            await delete_menu(menu_id)
        sheet.cell(row=row, column=menu_menu_id).value = None
        row += 1
    row = start_row
    while sheet.cell(row=row, column=submenu_menu_id).value:  # цикл для удаления подменю
        menu_id = sheet.cell(row=row, column=submenu_menu_id).value
        submenu_id = sheet.cell(row=row, column=submenu_submenu_id).value
        async with semaphore:
            await delete_submenu(menu_id, submenu_id)
        sheet.cell(row=row, column=submenu_menu_id).value = None
        sheet.cell(row=row, column=submenu_submenu_id).value = None
        row += 1
    row = start_row
    while sheet.cell(row=row, column=dish_menu_id).value:  # цикл для удаления блюд
        menu_id = sheet.cell(row=row, column=dish_menu_id).value
        submenu_id = sheet.cell(row=row, column=dish_submenu_id).value
        dish_id = sheet.cell(row=row, column=dish_dish_id).value
        async with semaphore:
            await delete_dish(menu_id, submenu_id, dish_id)
        sheet.cell(row=row, column=dish_menu_id).value = None
        sheet.cell(row=row, column=dish_submenu_id).value = None
        sheet.cell(row=row, column=dish_dish_id).value = None
        row += 1
    wb.save(filepath)
    wb.close()


celery_app = Celery('admin_task')

celery_app.conf.update(
    broker_url='pyamqp://guest:guest@rabbitmq:5672//',
    result_backend='rpc://',
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='Europe/Moscow',
    enable_utc=True,
    beat_schedule={
        'main': {
            'task': 'admin_task.main',
            'schedule': timedelta(seconds=15),
        },
    }
)


async def main_async() -> None:
    excel_path = 'admin/Menu.xlsx'
    await create_and_update_from_excel(excel_path)
    await delete_from_excel(excel_path, delete_row)


@celery_app.task
def main():
    result = loop.run_until_complete(main_async())
    return result


if __name__ == '__main__':
    asyncio.run(main_async())
