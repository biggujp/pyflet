import importlib, sys; m = importlib.import_module(f'module.ATCV1_PY{sys.version_info.major}{sys.version_info.minor}.ATCV1_PY{sys.version_info.major}{sys.version_info.minor}');globals()['ATCV1_PY'] = {k: v for k, v in {n: getattr(m, n) for n in dir(m) if n.startswith('pyarmor')}.items() if isinstance(v, type) and v.__name__.startswith('pyarmor__')};del m;

"""
  #### Python ง่ายนิดเดียว , © All Right Reserved ####
  #### Python ง่ายนิดเดียว , © All Right Reserved ####
  #### Python ง่ายนิดเดียว , © All Right Reserved ####

  * จำกัดการใช้งาน ใช้งานได้แค่ 2 เครื่องคอมพิวเตอร์เท่านั้น ( * แต่ถ้าแปลงเป็นไฟล์ .exe แล้วจะใช้งานกี่เครื่องก็ได้ไม่จำกัด และ ข้อความ License จะหายไปหากแปลงเป็นไฟล์ exe แล้ว )
  * Code อาจจะทำงานไม่ปกติถ้าหากไม่ได้ Run ใน Mode Run as Administrator *( วิธีทำคลิกขวาที่ไอคอน Visual Studio Code ที่ Desktop( หน้าจอคอม ) และเลือก Run as Administrator )
  * Code ตรวจจับภาพ และ ตรวจจับสี อาจจะทำงานไม่ปกติ ถ้าไม่ได้ตั้งขนาดหน้าจอ ( Scale and layout ) เป็น 100%

  เวอร์ชั่น 2.2 / 02-11-2024

"""

import numpy as np
import time
import cv2
import win32gui
import win32api
import win32ui
import win32con
import glob
import os
import ctypes
import pathlib
import sysconfig
import sys
import psutil

class tool_v1:

    # ==== Screenshot
    def screen_shot(filename=None, showdb=True, monitor_all=None):
        """

      พารามิเตอร์:
      - filename (str): ใส่ชื่อไฟล์ที่ต้องการ Save ( * ถ้าใส่ '' จะคืนค่ากลับมาเป็น Numpy )
      - showdb (bool): แสดงข้อมูลการทำงานของฟังก์ชัน (True = แสดงข้อมูลการทำงานของฟังก์ชัน , False = ไม่แสดงข้อมูลการทำงานของฟังก์ชัน)

      ผลลัพธ์:
      - ถ้า screenshot ได้สำเร็จจะคืนค่าออกมาเป็น None หรือ Numpy
      - ถ้า screenshot ไม่สำเร็จจะคืนค่ากลับมาเป็น False.

      """
        return globals()['ATCV1_PY']['pyarmor__68'].pyarmor__71(filename, showdb, monitor_all)

# === สำหรับ ค้นหารูปภาพ , ค้นหาสี , คลิก , พิมข้อความ
class autoclick_v1:

    # ==== หาตำแหน่งรูปภาพ
    def find_img(pic_local='', threshold_set=0.9, showimg=False, modecoler=False, rectangle_show=0.5, showdb=True, timeout=0, region=None, monitor_all=None):
        """

      พารามิเตอร์:
      - pic_local (str): ตำแหน่งรูปภาพที่ต้องการค้นหา
      - threshold_set (float): % ความน่าจะเป็นของการค้นหารูปภาพ
      - showimg (bool): แสดงภาพที่พบ (True = แสดงภาพที่พบ , False = ไม่แสดงภาพที่พบ)
      - modecoler (bool): True สำหรับค้นหาภาพแบบโหมด RGB, False สำหรับค้นหาภาพแบบโหมดขาวดำ.
      - rectangle_show (float): ต้องการตีกรอบสีเหลี่ยมสีแดงบนหน้าจอเมื่อค้นหาภาพเจอกี่วินาที *( ใส่ 0 = ไม่ต้องตีกรอบสีเหลี่ยม )
      - showdb (bool): แสดงข้อมูลการทำงานของฟังก์ชัน (True = แสดงข้อมูลการทำงานของฟังก์ชัน , False = ไม่แสดงข้อมูลการทำงานของฟังก์ชัน)
      - timeout (int): เวลาที่รอรูปภาพที่ต้องการหาปรากฏขึ้นมา (วินาที).
      - region (list[int, int, int, int]): กำหนดขอบเขตในการค้นหารูปภาพเฉพาะจุด. ( ถ้าใส่ None = ไม่ต้องการกำหนดขอบเขต )
      - monitor_all (None or int): กำหนดหน้าจอที่ต้องการค้นหาภาพ หรือ ค้นหาสี ( ถ้าใส่ None = ค้นหาทุกหน้าจอที่มี , ถ้าใส่ 1 = ค้นหาหน้าจอที่ 1 เท่านั้น )

      ผลลัพธ์:
      - ถ้าค้นหาเจอจะคืนค่ากลับมาเป็นตำแหน่งของรูปภาพ ในรูปแบบ list[]
      - ถ้าค้นหาไม่เจอจะคืนค่ากลับมาเป็น False.

      """
        return globals()['ATCV1_PY']['pyarmor__73'].pyarmor__76(pic_local, threshold_set, showimg, modecoler, rectangle_show, showdb, timeout, region, monitor_all)

    # ==== ค้นหาภาพหลายตำแหน่ง
    def find_img_muti(pic_local='', threshold_set=0.9, showimg=False, modecoler=False, rectangle_show=0.5, showdb=True, timeout=0, region=None, monitor_all=None):
        """

      พารามิเตอร์:
      - pic_local (str): ตำแหน่งรูปภาพที่ต้องการค้นหา
      - threshold_set (float): % ความน่าจะเป็นของการค้นหารูปภาพ
      - showimg (bool): แสดงภาพที่พบ (True = แสดงภาพที่พบ , False = ไม่แสดงภาพที่พบ)
      - modecoler (bool): True สำหรับค้นหาภาพแบบโหมด RGB, False สำหรับค้นหาภาพแบบโหมดขาวดำ.
      - rectangle_show (float): ต้องการตีกรอบสีเหลี่ยมสีแดงบนหน้าจอเมื่อค้นหาภาพเจอกี่วินาที *( ใส่ 0 = ไม่ต้องตีกรอบสีเหลี่ยม )
      - showdb (bool): แสดงข้อมูลการทำงานของฟังก์ชัน (True = แสดงข้อมูลการทำงานของฟังก์ชัน , False = ไม่แสดงข้อมูลการทำงานของฟังก์ชัน)
      - timeout (int): เวลาที่รอรูปภาพที่ต้องการหาปรากฏขึ้นมา (วินาที).
      - region (list[int, int, int, int]): กำหนดขอบเขตในการค้นหารูปภาพเฉพาะจุด. ( ถ้าใส่ None = ไม่ต้องการกำหนดขอบเขต )
      - monitor_all (None or int): กำหนดหน้าจอที่ต้องการค้นหาภาพ หรือ ค้นหาสี ( ถ้าใส่ None = ค้นหาทุกหน้าจอที่มี , ถ้าใส่ 1 = ค้นหาหน้าจอที่ 1 เท่านั้น )

      ผลลัพธ์:
      - ถ้าค้นหาเจอจะคืนค่ากลับมาเป็นตำแหน่งของรูปภาพ ในรูปแบบ list[]
      - ถ้าค้นหาไม่เจอจะคืนค่ากลับมาเป็น False.

      """
        return globals()['ATCV1_PY']['pyarmor__73'].pyarmor__78(pic_local, threshold_set, showimg, modecoler, rectangle_show, showdb, timeout, region, monitor_all)

    # ==== ค้นหาภาพหลายภาพ และ หลายตำแหน่ง
    def find_img_muti_file(pic_list=[''], threshold_set=0.9, showimg=False, modecoler=False, rectangle_show=0.5, showdb=True, timeout=0, region=None, monitor_all=None):
        """

      พารามิเตอร์:
      - pic_list (list[str,,]): ตำแหน่งรูปภาพที่ต้องการค้นหาใส่ได้หลายไฟล์
      - threshold_set (float): % ความน่าจะเป็นของการค้นหารูปภาพ
      - showimg (bool): แสดงภาพที่พบ (True = แสดงภาพที่พบ , False = ไม่แสดงภาพที่พบ)
      - modecoler (bool): True สำหรับค้นหาภาพแบบโหมด RGB, False สำหรับค้นหาภาพแบบโหมดขาวดำ.
      - rectangle_show (float): ต้องการตีกรอบสีเหลี่ยมสีแดงบนหน้าจอเมื่อค้นหาภาพเจอกี่วินาที *( ใส่ 0 = ไม่ต้องตีกรอบสีเหลี่ยม )
      - showdb (bool): แสดงข้อมูลการทำงานของฟังก์ชัน (True = แสดงข้อมูลการทำงานของฟังก์ชัน , False = ไม่แสดงข้อมูลการทำงานของฟังก์ชัน)
      - timeout (int): เวลาที่รอรูปภาพที่ต้องการหาปรากฏขึ้นมา (วินาที).
      - region (list[int, int, int, int]): กำหนดขอบเขตในการค้นหารูปภาพเฉพาะจุด. ( ถ้าใส่ None = ไม่ต้องการกำหนดขอบเขต )
      - monitor_all (None or int): กำหนดหน้าจอที่ต้องการค้นหาภาพ หรือ ค้นหาสี ( ถ้าใส่ None = ค้นหาทุกหน้าจอที่มี , ถ้าใส่ 1 = ค้นหาหน้าจอที่ 1 เท่านั้น )

      ผลลัพธ์:
      - ถ้าค้นหาเจอจะคืนค่ากลับมาเป็นตำแหน่งของรูปภาพ ในรูปแบบ list[]
      - ถ้าค้นหาไม่เจอจะคืนค่ากลับมาเป็น False.

      """
        return globals()['ATCV1_PY']['pyarmor__73'].pyarmor__80(pic_list, threshold_set, showimg, modecoler, rectangle_show, showdb, timeout, region, monitor_all)

    # ==== ค้นหาไฟล์ในโฟรเดอร์ทั้งหมด และ หลายตำแหน่ง
    def find_img_muti_in_folder(folder='', threshold_set=0.9, showimg=False, modecoler=False, rectangle_show=0.5, showdb=True, timeout=0, region=None, monitor_all=None):
        """

      พารามิเตอร์:
      - folder (list[str]): โฟรเดอร์ที่เก็บรูปภาพ
      - threshold_set (float): % ความน่าจะเป็นของการค้นหารูปภาพ
      - showimg (bool): แสดงภาพที่พบ (True = แสดงภาพที่พบ , False = ไม่แสดงภาพที่พบ)
      - modecoler (bool): True สำหรับค้นหาภาพแบบโหมด RGB, False สำหรับค้นหาภาพแบบโหมดขาวดำ.
      - rectangle_show (float): ต้องการตีกรอบสีเหลี่ยมสีแดงบนหน้าจอเมื่อค้นหาภาพเจอกี่วินาที *( ใส่ 0 = ไม่ต้องตีกรอบสีเหลี่ยม )
      - showdb (bool): แสดงข้อมูลการทำงานของฟังก์ชัน (True = แสดงข้อมูลการทำงานของฟังก์ชัน , False = ไม่แสดงข้อมูลการทำงานของฟังก์ชัน)
      - timeout (int): เวลาที่รอรูปภาพที่ต้องการหาปรากฏขึ้นมา (วินาที).
      - region (list[int, int, int, int]): กำหนดขอบเขตในการค้นหารูปภาพเฉพาะจุด. ( ถ้าใส่ None = ไม่ต้องการกำหนดขอบเขต )
      - monitor_all (None or int): กำหนดหน้าจอที่ต้องการค้นหาภาพ หรือ ค้นหาสี ( ถ้าใส่ None = ค้นหาทุกหน้าจอที่มี , ถ้าใส่ 1 = ค้นหาหน้าจอที่ 1 เท่านั้น )

      ผลลัพธ์:
      - ถ้าค้นหาเจอจะคืนค่ากลับมาเป็นตำแหน่งของรูปภาพ ในรูปแบบ list[]
      - ถ้าค้นหาไม่เจอจะคืนค่ากลับมาเป็น False.

      """
        return globals()['ATCV1_PY']['pyarmor__73'].pyarmor__82(folder, threshold_set, showimg, modecoler, rectangle_show, showdb, timeout, region, monitor_all)

    # ==== รอโหลดรูปภาพ
    def load_img(pic_local='', threshold_set=0.9, timeout=0.5, showimg=False, modecoler=False, showdb=True, region=None, monitor_all=None):
        """

      พารามิเตอร์:
      - pic_local (str): ตำแหน่งรูปภาพที่ต้องการค้นหา
      - threshold_set (float): % ความน่าจะเป็นของการค้นหารูปภาพ
      - showimg (bool): แสดงภาพที่พบ (True = แสดงภาพที่พบ , False = ไม่แสดงภาพที่พบ)
      - modecoler (bool): True สำหรับค้นหาภาพแบบโหมด RGB, False สำหรับค้นหาภาพแบบโหมดขาวดำ.
      - showdb (bool): แสดงข้อมูลการทำงานของฟังก์ชัน (True = แสดงข้อมูลการทำงานของฟังก์ชัน , False = ไม่แสดงข้อมูลการทำงานของฟังก์ชัน)
      - timeout (int): เวลาที่รอรูปภาพที่ต้องการหาปรากฏขึ้นมา (วินาที).
      - region (list[int, int, int, int]): กำหนดขอบเขตในการค้นหารูปภาพเฉพาะจุด. ( ถ้าใส่ None = ไม่ต้องการกำหนดขอบเขต )
      - monitor_all (None or int): กำหนดหน้าจอที่ต้องการค้นหาภาพ หรือ ค้นหาสี ( ถ้าใส่ None = ค้นหาทุกหน้าจอที่มี , ถ้าใส่ 1 = ค้นหาหน้าจอที่ 1 เท่านั้น )

      ผลลัพธ์:
      - ถ้าค้นหาเจอจะคืนค่ากลับมาเป็นตำแหน่งของรูปภาพ ในรูปแบบ list[]
      - ถ้าค้นหาไม่เจอจะคืนค่ากลับมาเป็น False.

      """
        return globals()['ATCV1_PY']['pyarmor__73'].pyarmor__84(pic_local, threshold_set, timeout, showimg, modecoler, showdb, region, monitor_all)

    # ==== ค้นหาสี
    def find_pixel(local=[], hex_coler='', shade=5, showdb=True, timeout=0, monitor_all=None):
        """

      พารามิเตอร์:
      - local (list[int,int]): ตำแหน่งที่ต้องการตรวจสอบสี
      - hex_coler (str): ค่าสีรูปแบบ Hex
      - shade (int): ความใกล้เคียงของสี
      - showdb (bool): แสดงข้อมูลการทำงานของฟังก์ชัน (True = แสดงข้อมูลการทำงานของฟังก์ชัน , False = ไม่แสดงข้อมูลการทำงานของฟังก์ชัน)
      - timeout (int): เวลาที่รอสีที่ต้องการหาปรากฏขึ้นมา (วินาที).
      - monitor_all (None or int): กำหนดหน้าจอที่ต้องการค้นหาภาพ หรือ ค้นหาสี ( ถ้าใส่ None = ค้นหาทุกหน้าจอที่มี , ถ้าใส่ 1 = ค้นหาหน้าจอที่ 1 เท่านั้น )

      ผลลัพธ์:
      - ถ้าค้นหาเจอจะคืนค่ากลับมาเป็นตำแหน่งสี [x, y]
      - ถ้าไม่เจอจะคืนค่ากลับมาเป็น False.

      """
        return globals()['ATCV1_PY']['pyarmor__73'].pyarmor__86(local, hex_coler, shade, showdb, timeout, monitor_all)

    # ==== ค้นหาสี หลายจุด
    def find_pixel_match(local_list=[], hex_coler_list=[], shade=5, showdb=True, timeout=0, monitor_all=None):
        """

      พารามิเตอร์:
      - local_list (List[List[int,int],,]): ตำแหน่งที่ต้องการเช็คสี
      - hex_coler_list (List[str,,]): ค่า Hex ของสีที่ต้องการหา
      - shade (int): ความเพี้ยนของสีที่ยอมรับ
      - showdb (bool): แสดงข้อมูลการทำงานของฟังก์ชัน (True = แสดงข้อมูลการทำงานของฟังก์ชัน , False = ไม่แสดงข้อมูลการทำงานของฟังก์ชัน)
      - timeout (int): เวลาที่รอสีที่ต้องการหาปรากฏขึ้นมา (วินาที)
      - monitor_all (None or int): กำหนดหน้าจอที่ต้องการค้นหาภาพ หรือ ค้นหาสี ( ถ้าใส่ None = ค้นหาทุกหน้าจอที่มี , ถ้าใส่ 1 = ค้นหาหน้าจอที่ 1 เท่านั้น )

      ผลลัพธ์:
      - ถ้าค้นหาเจอจะคืนค่ากลับมาเป็นตำแหน่งสี [x, y]
      - ถ้าไม่เจอจะคืนค่ากลับมาเป็น False.

      """
        return globals()['ATCV1_PY']['pyarmor__73'].pyarmor__88(local_list, hex_coler_list, shade, showdb, timeout, monitor_all)

    # ==== ค้นหาสีแบบ range
    def find_pixel_range(local_list_range=[[0, 0], [10, 10]], hex_coler='', shade=5, showdb=True, timeout=0, step=1, monitor_all=None):
        """

      พารามิเตอร์:
      - local_list_range ( List[ list[ int,int ] , list[ int,int ] ]  ): ตำแหน่งเริ่มต้น และ สิ้นสุด ที่จะค้นหา 
      - hex_coler (str): ค่า Hex ของสีที่ต้องการหา
      - shade (int):ความเพี้ยนของสีที่ยอมรับ
      - step (int): ความถี่ในการตรวจสอบ
      - showdb (bool): แสดงข้อมูลการทำงานของฟังก์ชัน (True = แสดงข้อมูลการทำงานของฟังก์ชัน , False = ไม่แสดงข้อมูลการทำงานของฟังก์ชัน)
      - timeout (int): เวลาที่รอสีที่ต้องการหาปรากฏขึ้นมา (วินาที)
      - monitor_all (None or int): กำหนดหน้าจอที่ต้องการค้นหาภาพ หรือ ค้นหาสี ( ถ้าใส่ None = ค้นหาทุกหน้าจอที่มี , ถ้าใส่ 1 = ค้นหาหน้าจอที่ 1 เท่านั้น )
  
      ผลลัพธ์:
      - ถ้าค้นหาเจอจะคืนค่ากลับมาเป็นตำแหน่งสี [x, y]
      - ถ้าไม่เจอจะคืนค่ากลับมาเป็น False.

      """
        check_coler = globals()['ATCV1_PY']['pyarmor__73'].pyarmor__90(local_list_range, hex_coler, shade, showdb, timeout, step, monitor_all)
        if check_coler is None:
            return False
        else:
            return check_coler

    # ==== ค้นหาสีแบบ Box
    def find_pixel_box(local_box=[0, 0, 100, 100], hex_coler_list=[], shade=5, showdb=True, timeout=0, step=1, monitor_all=None):
        """

      พารามิเตอร์:
      - local_box (List[int,int,int,int]): ตำแหน่งรูปแบบสี่เหลี่ยม ( นำค่ามาจากโปรแกรม screen short ) ที่ต้องการค้นหาสี 
      - hex_coler_list (List[str,,]): รายการค่า Hex สีจาก Autoit ที่ต้องการค้นหา 
      - shade (int): ความเพี้ยนของสีที่ยอมรับ
      - showdb (bool): แสดงข้อมูลการทำงานของฟังก์ชัน (True = แสดงข้อมูลการทำงานของฟังก์ชัน , False = ไม่แสดงข้อมูลการทำงานของฟังก์ชัน)
      - timeout (int): เวลาที่รอสีที่ต้องการหาปรากฏขึ้นมา (วินาที)
      - step (int): ความถี่ในการตรวจสอบ 
      - monitor_all (None or int): กำหนดหน้าจอที่ต้องการค้นหาภาพ หรือ ค้นหาสี ( ถ้าใส่ None = ค้นหาทุกหน้าจอที่มี , ถ้าใส่ 1 = ค้นหาหน้าจอที่ 1 เท่านั้น )

      ผลลัพธ์:
      - ถ้าค้นหาเจอจะคืนค่ากลับมาเป็นตำแหน่งสี [x, y]
      - ถ้าไม่เจอจะคืนค่ากลับมาเป็น False.

      """
        return globals()['ATCV1_PY']['pyarmor__73'].pyarmor__92(local_box, hex_coler_list, shade, showdb, timeout, step, monitor_all)

    # ==== หาตำแหน่งรูปภาพ และ คลิก
    def find_img_and_click(pic_local='', threshold_set=0.9, showimg=False, modecoler=False, rectangle_show=0.5, showdb=True, timeout=0, region=None, lv_click=1, monitor_all=None):
        """

        พารามิเตอร์:
        - pic_local (str): ตำแหน่งไฟล์ภาพ
        - lv_click (int): จำนวนครั้งที่ต้องการคลิก
        - timeout (int):  เวลาที่รอรูปภาพที่ต้องการหาปรากฏขึ้นมา (ในวินาที).
        - threshold_set (float): ค่าความน่าจะเป็นสำหรับการตรวจจับภาพ.
        - showimg (bool): แสดงภาพที่พบ (True = แสดงภาพที่พบ , False = ไม่แสดงภาพที่พบ)
        - rectangle_show (float): ต้องการตีกรอบสี่เหลี่ยมบนหน้าจอนานกี่วินาที , ถ้าใส่ 0 = ไม่ต้องตีกรอบ.
        - showdb (bool): แสดงข้อมูลการทำงานของฟังก์ชัน (True = แสดงข้อมูลการทำงานของฟังก์ชัน , False = ไม่แสดงข้อมูลการทำงานของฟังก์ชัน)
        - modecoler (bool): โหมดค้นหาภาพ (False = ค้นหาภาพโหมด RGB, True = ค้นหาภาพแบบขาวดำ)
        - region (list[int, int, int, int]): กำหนดขอบเขตในการค้นหารูปภาพเฉพาะจุด. ( ถ้าใส่ None = ไม่ต้องการกำหนดขอบเขต )
        - monitor_all (None or int): กำหนดหน้าจอที่ต้องการค้นหาภาพ หรือ ค้นหาสี ( ถ้าใส่ None = ค้นหาทุกหน้าจอที่มี , ถ้าใส่ 1 = ค้นหาหน้าจอที่ 1 เท่านั้น )
    
        ผลลัพธ์:
        - ถ้าค้นหาเจอจะคืนค่ากลับมาเป็น True
        - ถ้าไม่เจอจะคืนค่ากลับมาเป็น False.

        """
        detect = autoclick_v1.find_img(pic_local, threshold_set, showimg, modecoler, rectangle_show, showdb, timeout, region, monitor_all)
        if detect != False:
            return autoclick_v1.click(globals()['ATCV1_PY']['pyarmor__73'].pyarmor__74(*detect), lv_click, showdb)
        return False

    # ==== หาตำแหน่งรูปภาพทั้งหมด และ คลิกทั้งหมด
    def find_img_and_click_muti(pic_local='', threshold_set=0.9, showimg=False, modecoler=False, rectangle_show=0.5, showdb=True, timeout=0, region=None, lv_click=1, delay_click=0.05, monitor_all=None):
        """

        พารามิเตอร์:
        - pic_local (str): ตำแหน่งไฟล์ภาพ
        - lv_click (int): จำนวนครั้งที่ต้องการคลิก
        - timeout (int):  เวลาที่รอรูปภาพที่ต้องการหาปรากฏขึ้นมา (ในวินาที).
        - threshold_set (float): ค่าความน่าจะเป็นสำหรับการตรวจจับภาพ.
        - showimg (bool): แสดงภาพที่พบ (True = แสดงภาพที่พบ , False = ไม่แสดงภาพที่พบ)
        - rectangle_show (float): ต้องการตีกรอบสี่เหลี่ยมบนหน้าจอนานกี่วินาที , ถ้าใส่ 0 = ไม่ต้องตีกรอบ.
        - showdb (bool): แสดงข้อมูลการทำงานของฟังก์ชัน (True = แสดงข้อมูลการทำงานของฟังก์ชัน , False = ไม่แสดงข้อมูลการทำงานของฟังก์ชัน)
        - modecoler (bool): โหมดค้นหาภาพ (False = ค้นหาภาพโหมด RGB, True = ค้นหาภาพแบบขาวดำ)
        - region (list[int, int, int, int]): กำหนดขอบเขตในการค้นหารูปภาพเฉพาะจุด. ( ถ้าใส่ None = ไม่ต้องการกำหนดขอบเขต )
        - delay_click (int):  ความเร็วในการคลิกรูปภาพที่หาเจอทั้งหมด (ในวินาที).
        - monitor_all (None or int): กำหนดหน้าจอที่ต้องการค้นหาภาพ หรือ ค้นหาสี ( ถ้าใส่ None = ค้นหาทุกหน้าจอที่มี , ถ้าใส่ 1 = ค้นหาหน้าจอที่ 1 เท่านั้น )

        ผลลัพธ์:
        - ถ้าค้นหาเจอจะคืนค่ากลับมาเป็น True
        - ถ้าไม่เจอจะคืนค่ากลับมาเป็น False.

        """
        detect = autoclick_v1.find_img_muti(pic_local, threshold_set, showimg, modecoler, rectangle_show, showdb, timeout, region, monitor_all)
        if detect != False:
            if len(detect) > 0:
                for var in detect:
                    if autoclick_v1.click(globals()['ATCV1_PY']['pyarmor__73'].pyarmor__74(*var), lv_click, showdb) == False:
                        return False
                    time.sleep(delay_click)
                    return True
            else:
                return autoclick_v1.click(detect[0], lv_click, showdb)
        return False

    # ==== หาตำแหน่งรูปภาพหลายภาพ และ คลิกทั้งหมด
    def find_img_and_click_muti_file(pic_list=[''], threshold_set=0.9, showimg=False, modecoler=False, rectangle_show=0.5, showdb=True, timeout=0, region=None, lv_click=1, delay_click=0.05, monitor_all=None):
        """

        พารามิเตอร์:
        - pic_list (List[str,,]): ตำแหน่งไฟล์ภาพ
        - lv_click (int): จำนวนครั้งที่ต้องการคลิก
        - timeout (int):  เวลาที่รอรูปภาพที่ต้องการหาปรากฏขึ้นมา (ในวินาที).
        - threshold_set (float): ค่าความน่าจะเป็นสำหรับการตรวจจับภาพ.
        - showimg (bool): แสดงภาพที่พบ (True = แสดงภาพที่พบ , False = ไม่แสดงภาพที่พบ)
        - rectangle_show (float): ต้องการตีกรอบสี่เหลี่ยมบนหน้าจอนานกี่วินาที , ถ้าใส่ 0 = ไม่ต้องตีกรอบ.
        - showdb (bool): แสดงข้อมูลการทำงานของฟังก์ชัน (True = แสดงข้อมูลการทำงานของฟังก์ชัน , False = ไม่แสดงข้อมูลการทำงานของฟังก์ชัน)
        - modecoler (bool): โหมดค้นหาภาพ (False = ค้นหาภาพโหมด RGB, True = ค้นหาภาพแบบขาวดำ)
        - region (list[int, int, int, int]): กำหนดขอบเขตในการค้นหารูปภาพเฉพาะจุด. ( ถ้าใส่ None = ไม่ต้องการกำหนดขอบเขต )
        - delay_click (int):  ความเร็วในการคลิกรูปภาพที่หาเจอทั้งหมด (ในวินาที).
        - monitor_all (None or int): กำหนดหน้าจอที่ต้องการค้นหาภาพ หรือ ค้นหาสี ( ถ้าใส่ None = ค้นหาทุกหน้าจอที่มี , ถ้าใส่ 1 = ค้นหาหน้าจอที่ 1 เท่านั้น )
        
        ผลลัพธ์:
        - ถ้าค้นหาเจอจะคืนค่ากลับมาเป็น True
        - ถ้าไม่เจอจะคืนค่ากลับมาเป็น False.

        """
        detect = autoclick_v1.find_img_muti_file(pic_list, threshold_set, showimg, modecoler, rectangle_show, showdb, timeout, region, monitor_all)
        if detect != False:
            if len(detect) > 0:
                if type(detect[0]) == list:
                    for var in detect:
                        if autoclick_v1.click(globals()['ATCV1_PY']['pyarmor__73'].pyarmor__74(*var), lv_click, showdb) == False:
                            return False
                        time.sleep(delay_click)
                    return True
                else:
                    return autoclick_v1.click(globals()['ATCV1_PY']['pyarmor__73'].pyarmor__74(*detect), lv_click, showdb)
        return False

    # ==== หาตำแหน่งรูปภาพหลายภาพในโฟรเดอร์ และ คลิกทั้งหมด
    def find_img_and_click_muti_in_folder(folder='', threshold_set=0.9, showimg=False, modecoler=False, rectangle_show=0.5, showdb=True, timeout=0, region=None, lv_click=1, delay_click=0.05, monitor_all=None):
        """

        พารามิเตอร์:
        - folder (str): ตำแหน่งโฟรเดอร์ที่เก็บไฟล์ภาพ
        - lv_click (int): จำนวนครั้งที่ต้องการคลิก
        - timeout (int):  เวลาที่รอรูปภาพที่ต้องการหาปรากฏขึ้นมา (ในวินาที).
        - delay_click (int):  ความเร็วในการคลิกรูปภาพที่หาเจอทั้งหมด (ในวินาที).
        - threshold_set (float): ค่าความน่าจะเป็นสำหรับการตรวจจับภาพ.
        - showimg (bool): แสดงภาพที่พบ (True = แสดงภาพที่พบ , False = ไม่แสดงภาพที่พบ)
        - rectangle_show (float): ต้องการตีกรอบสี่เหลี่ยมบนหน้าจอนานกี่วินาที , ถ้าใส่ 0 = ไม่ต้องตีกรอบ.
        - showdb (bool): แสดงข้อมูลการทำงานของฟังก์ชัน (True = แสดงข้อมูลการทำงานของฟังก์ชัน , False = ไม่แสดงข้อมูลการทำงานของฟังก์ชัน)
        - modecoler (bool): โหมดค้นหาภาพ (False = ค้นหาภาพโหมด RGB, True = ค้นหาภาพแบบขาวดำ)
        - region (list[int, int, int, int]): กำหนดขอบเขตในการค้นหารูปภาพเฉพาะจุด. ( ถ้าใส่ None = ไม่ต้องการกำหนดขอบเขต )
        - monitor_all (None or int): กำหนดหน้าจอที่ต้องการค้นหาภาพ หรือ ค้นหาสี ( ถ้าใส่ None = ค้นหาทุกหน้าจอที่มี , ถ้าใส่ 1 = ค้นหาหน้าจอที่ 1 เท่านั้น )

        ผลลัพธ์:
        - ถ้าค้นหาเจอจะคืนค่ากลับมาเป็น True
        - ถ้าไม่เจอจะคืนค่ากลับมาเป็น False.

        """
        detect = autoclick_v1.find_img_muti_in_folder(folder, threshold_set, showimg, modecoler, rectangle_show, showdb, timeout, region, monitor_all)
        if detect != False:
            if len(detect) > 0:
                if type(detect[0]) == list:
                    for var in detect:
                        if autoclick_v1.click(globals()['ATCV1_PY']['pyarmor__73'].pyarmor__74(*var), lv_click, showdb) == False:
                            return False
                        time.sleep(delay_click)
                    return True
                else:
                    return autoclick_v1.click(globals()['ATCV1_PY']['pyarmor__73'].pyarmor__74(*detect), lv_click, showdb)
        return False

    # == เทียบสีจุดเดียว และ คลิก
    def find_pixel_and_click(local=[], hex_coler='', shade=5, showdb=True, timeout=0, lv_click=1, monitor_all=None):
        """

        พารามิเตอร์:
        - local (List[int,int]): ตำแหน่งที่ต้องการเช็คสี
        - hex_coler (str): ค่า Hex ของสีที่ต้องการหา
        - shade (int): ความเพี้ยนของสีที่ยอมรับ
        - lv_click (int): จำนวนครั้งที่ต้องการคลิก
        - showdb (bool): แสดงข้อมูลการทำงานของฟังก์ชัน (True = แสดงข้อมูลการทำงานของฟังก์ชัน , False = ไม่แสดงข้อมูลการทำงานของฟังก์ชัน)
        - timeout (int): เวลาที่รอสีที่ต้องการหาปรากฏขึ้นมา (วินาที).
        - monitor_all (None or int): กำหนดหน้าจอที่ต้องการค้นหาภาพ หรือ ค้นหาสี ( ถ้าใส่ None = ค้นหาทุกหน้าจอที่มี , ถ้าใส่ 1 = ค้นหาหน้าจอที่ 1 เท่านั้น )

        ผลลัพธ์:
        - ถ้าค้นหาเจอจะคืนค่ากลับมาเป็น True
        - ถ้าไม่เจอจะคืนค่ากลับมาเป็น False.

        """
        detect = autoclick_v1.find_pixel(local, hex_coler, shade, showdb, timeout, monitor_all)
        if detect != False:
            return autoclick_v1.click(detect, lv_click, showdb)
        return False

    # == เทียบสีหลายจุด และ คลิก
    def find_pixel_match_and_click(local_list=[], hex_coler_list=[], shade=5, showdb=True, timeout=0, lv_click=1, monitor_all=None):
        """

        พารามิเตอร์:
        - local_list (List[List[int,int],,]): ตำแหน่งที่ต้องการเช็คสี
        - hex_coler_list (List[str,,]): ค่า Hex ของสีที่ต้องการหา
        - shade (int): ความเพี้ยนของสีที่ยอมรับ
        - lv_click (int): จำนวนครั้งที่ต้องการคลิก
        - showdb (bool): แสดงข้อมูลการทำงานของฟังก์ชัน (True = แสดงข้อมูลการทำงานของฟังก์ชัน , False = ไม่แสดงข้อมูลการทำงานของฟังก์ชัน)
        - timeout (int): เวลาที่รอสีที่ต้องการหาปรากฏขึ้นมา (วินาที)
        - monitor_all (None or int): กำหนดหน้าจอที่ต้องการค้นหาภาพ หรือ ค้นหาสี ( ถ้าใส่ None = ค้นหาทุกหน้าจอที่มี , ถ้าใส่ 1 = ค้นหาหน้าจอที่ 1 เท่านั้น )
    
        ผลลัพธ์:
        - ถ้าค้นหาเจอจะคืนค่ากลับมาเป็น True
        - ถ้าไม่เจอจะคืนค่ากลับมาเป็น False.

        """
        detect = autoclick_v1.find_pixel_match(local_list, hex_coler_list, shade, showdb, timeout, monitor_all)
        if detect != False:
            return autoclick_v1.click(detect, lv_click, showdb)
        return False

    # == เทียบสีแบบเส้นตรง และ คลิก
    def find_pixel_range_and_click(local_list_range=[[0, 0], [10, 10]], hex_coler='', shade=5, showdb=True, timeout=0, step=1, lv_click=1, monitor_all=None):
        """

        พารามิเตอร์:
        - local_list_range ( List[ list[ int,int ] , list[ int,int ] ]  ): ตำแหน่งเริ่มต้น และ สิ้นสุด ที่จะค้นหา 
        - hex_coler (str): ค่า Hex ของสีที่ต้องการหา
        - shade (int):ความเพี้ยนของสีที่ยอมรับ
        - step (int): ความถี่ในการตรวจสอบ
        - lv_click (int): จำนวนครั้งที่ต้องการคลิก
        - timeout (int): เวลาที่รอสีที่ต้องการหาปรากฏขึ้นมา (วินาที)
        - showdb (bool): แสดงข้อมูลการทำงานของฟังก์ชัน (True = แสดงข้อมูลการทำงานของฟังก์ชัน , False = ไม่แสดงข้อมูลการทำงานของฟังก์ชัน)
        - monitor_all (None or int): กำหนดหน้าจอที่ต้องการค้นหาภาพ หรือ ค้นหาสี ( ถ้าใส่ None = ค้นหาทุกหน้าจอที่มี , ถ้าใส่ 1 = ค้นหาหน้าจอที่ 1 เท่านั้น )

        ผลลัพธ์:
        - ถ้าค้นหาเจอจะคืนค่ากลับมาเป็น True
        - ถ้าไม่เจอจะคืนค่ากลับมาเป็น False.

        """
        detect = autoclick_v1.find_pixel_range(local_list_range, hex_coler, shade, showdb, timeout, step, monitor_all)
        if detect != False:
            return autoclick_v1.click(detect, lv_click, showdb)
        return False

    # == เทียบสีรูปแบบสี่เหลี่ยม และ คลิก
    def find_pixel_box_and_click(local_box=[0, 0, 100, 100], hex_coler_list=[], shade=5, showdb=True, timeout=0, step=1, lv_click=1, monitor_all=None):
        """

        พารามิเตอร์:
        - local_box (List[int,int,int,int]): ตำแหน่งของกล่องที่ต้องการค้นหาสี 
        - hex_coler_list (List[str,,]): รายการค่า Hex สีจาก Autoit ที่ต้องการค้นหา 
        - shade (int): ความเพี้ยนของสีที่ยอมรับ
        - showdb (bool): แสดงข้อมูลการทำงานของฟังก์ชัน (True = แสดงข้อมูลการทำงานของฟังก์ชัน , False = ไม่แสดงข้อมูลการทำงานของฟังก์ชัน)
        - timeout (int): เวลาที่รอสีที่ต้องการหาปรากฏขึ้นมา (วินาที)
        - step (int): ความถี่ในการตรวจสอบ 
        - lv_click (int): จำนวนครั้งที่ต้องการคลิก
        - monitor_all (None or int): กำหนดหน้าจอที่ต้องการค้นหาภาพ หรือ ค้นหาสี ( ถ้าใส่ None = ค้นหาทุกหน้าจอที่มี , ถ้าใส่ 1 = ค้นหาหน้าจอที่ 1 เท่านั้น )

        ผลลัพธ์:
        - ถ้าค้นหาเจอจะคืนค่ากลับมาเป็น True
        - ถ้าไม่เจอจะคืนค่ากลับมาเป็น False.

        """
        detect = autoclick_v1.find_pixel_box(local_box, hex_coler_list, shade, showdb, timeout, step, monitor_all)
        if detect != False:
            return autoclick_v1.click(detect, lv_click, showdb)
        return False

    # ==== คลิกซ้าย X
    def click(local=[], lv_click=1, showdb=True):
        """

      พารามิเตอร์:
      - local (List[int,int]): ตำแหน่งที่ต้องการคลิก
      - lv_click (int): จำนวนครั้งที่ต้องการคลิก
      - showdb (bool): แสดงข้อมูลการทำงานของฟังก์ชัน (True = แสดงข้อมูลการทำงานของฟังก์ชัน , False = ไม่แสดงข้อมูลการทำงานของฟังก์ชัน)

      ผลลัพธ์:
      - ถ้าคลิกสำเร็จจะคืนค่าเป็น True
      - ถ้าคลิกไม่สำเร็จจะคืนค่าเป็น False.

      """
        return globals()['ATCV1_PY']['pyarmor__73'].pyarmor__94(local, lv_click, showdb)

    # ==== ตั้ง Cursor
    def set_cursor_mouse(local=[], showdb=True):
        """

      พารามิเตอร์:
      - local (List[int,int]): ตำแหน่งที่ต้องการตั้ง cursor
      - showdb (bool): แสดงข้อมูลการทำงานของฟังก์ชัน (True = แสดงข้อมูลการทำงานของฟังก์ชัน , False = ไม่แสดงข้อมูลการทำงานของฟังก์ชัน)

      ผลลัพธ์:
      - ถ้าตั้ง cursor สำเร็จจะคืนค่าเป็น True
      - ถ้าตั้ง cursor ไม่สำเร็จจะคืนค่าเป็น False.

      """
        return globals()['ATCV1_PY']['pyarmor__73'].pyarmor__96(local, showdb)

    # ==== คลิกค้าง
    def click_event_down(event=2, showdb=True):
        """

      # คลิก ซ้ายค้าง = 2
      # คลิก ขวาค้าง = 8
      # คลิก กลางเมาส์ค้าง = 32

      พารามิเตอร์:
      - event (int): เลข EventMouse ด้านบน
      - showdb (bool): แสดงข้อมูลการทำงานของฟังก์ชัน (True = แสดงข้อมูลการทำงานของฟังก์ชัน , False = ไม่แสดงข้อมูลการทำงานของฟังก์ชัน)

      ผลลัพธ์:
      - ถ้าคลิกสำเร็จจะคืนค่าเป็น True
      - ถ้าคลิกไม่สำเร็จจะคืนค่าเป็น False.

      """
        return globals()['ATCV1_PY']['pyarmor__73'].pyarmor__98(event, showdb)

    # ==== ปล่อยคลิก
    def click_event_up(event=4, showdb=True):
        """

      # ปล่อย คลิกซ้าย = 4
      # ปล่อย คลิกขวา = 16
      # ปล่อย คลิกกลางเมาส์ = 64

      พารามิเตอร์:
      - event (int): เลข EventMouse ด้านบน
      - showdb (bool): แสดงข้อมูลการทำงานของฟังก์ชัน (True = แสดงข้อมูลการทำงานของฟังก์ชัน , False = ไม่แสดงข้อมูลการทำงานของฟังก์ชัน)

      ผลลัพธ์:
      - ถ้าคลิกสำเร็จจะคืนค่าเป็น True
      - ถ้าคลิกไม่สำเร็จจะคืนค่าเป็น False.

      """
        return globals()['ATCV1_PY']['pyarmor__73'].pyarmor__100(event, showdb)

    # ==== ย้ายเมาส์
    def move_mouse(first=[], last=[], speed=1, showdb=True):
        """

      พารามิเตอร์:
      - first (List[int,int]): ตำแหน่งเริ่มต้นที่จะต้องการคลิกและลากเมาส์
      - last (List[int,int]): ตำแหน่งสิ้นสุดที่จะคลิกและลากเมาส์
      - speed (int): ความเร็วในการเลื่อนเมาส์
      - showdb (bool): แสดงข้อมูลการทำงานของฟังก์ชัน (True = แสดงข้อมูลการทำงานของฟังก์ชัน , False = ไม่แสดงข้อมูลการทำงานของฟังก์ชัน)

      ผลลัพธ์:
      - ถ้า move_mouse สำเร็จจะคืนค่าเป็น True
      - ถ้า move_mouse ไม่สำเร็จจะคืนค่าเป็น False.

      """
        return globals()['ATCV1_PY']['pyarmor__73'].pyarmor__102(first, last, speed, showdb)

    # ==== คลิกและลากวาง
    def drag_mouse(first=[], last=[], speed=1, showdb=True):
        """

      พารามิเตอร์:
      - first (List[int,int]): ตำแหน่งเริ่มต้นที่จะต้องการคลิกและลากเมาส์
      - last (List[int,int]): ตำแหน่งสิ้นสุดที่จะคลิกและลากเมาส์
      - speed (int): ความเร็วในการเลื่อนเมาส์
      - showdb (bool): แสดงข้อมูลการทำงานของฟังก์ชัน (True = แสดงข้อมูลการทำงานของฟังก์ชัน , False = ไม่แสดงข้อมูลการทำงานของฟังก์ชัน)

      ผลลัพธ์:
      - คลิกและลากเมาส์ สำเร็จจะคืนค่าเป็น True
      - คลิกและลากเมาส์ ไม่สำเร็จจะคืนค่าเป็น False.

      """
        return globals()['ATCV1_PY']['pyarmor__73'].pyarmor__104(first, last, speed, showdb)

    # ==== คลิกและลากวางและกดค้าง
    def drag_mouse_and_hold(first=[], last=[], speed=1, timeout=1, showdb=True):
        """

      พารามิเตอร์:
      - first (List[int,int]): ตำแหน่งเริ่มต้นที่จะต้องการคลิกและลากเมาส์
      - last (List[int,int]): ตำแหน่งสิ้นสุดที่จะคลิกและลากเมาส์
      - speed (int): ความเร็วในการเลื่อนเมาส์
      - timeout (int): ต้องการลากเมาส์ค้างไว้กี่วินาที
      - showdb (bool): แสดงข้อมูลการทำงานของฟังก์ชัน (True = แสดงข้อมูลการทำงานของฟังก์ชัน , False = ไม่แสดงข้อมูลการทำงานของฟังก์ชัน)

      ผลลัพธ์:
      - คลิกและลากเมาส์ สำเร็จจะคืนค่าเป็น True
      - คลิกและลากเมาส์ ไม่สำเร็จจะคืนค่าเป็น False.

      """
        return globals()['ATCV1_PY']['pyarmor__73'].pyarmor__106(first, last, speed, timeout, showdb)

    # ==== พักการทำงาน
    def delay(time_input=0.5, showdb=True):
        """

      พารามิเตอร์:
      - time_input (float): วินาทีที่ต้องการให้บอทพักการทำงาน
      - showdb (bool): แสดงข้อมูลการทำงานของฟังก์ชัน (True = แสดงข้อมูลการทำงานของฟังก์ชัน , False = ไม่แสดงข้อมูลการทำงานของฟังก์ชัน)

      """
        return globals()['ATCV1_PY']['pyarmor__73'].pyarmor__108(time_input, showdb)

    # ==== จับเวลา
    def timeset(timeset=1, showdb=True):
        """

      พารามิเตอร์:
      - timeset (int): วินาทีที่ต้องการจับเวลา
      - showdb (bool): แสดงข้อมูลการทำงานของฟังก์ชัน (True = แสดงข้อมูลการทำงานของฟังก์ชัน , False = ไม่แสดงข้อมูลการทำงานของฟังก์ชัน)

      ผลลัพธ์:
      - คืนค่าออกมาเป็น time unix

      """
        return globals()['ATCV1_PY']['pyarmor__73'].pyarmor__110(timeset, showdb)

    # ==== หมดเวลา
    def timeout(timeout=1, showdb=True):
        """

      พารามิเตอร์:
      - timeout (int): ค่า time unix จากฟังก์ชั่น timeset
      - showdb (bool): แสดงข้อมูลการทำงานของฟังก์ชัน (True = แสดงข้อมูลการทำงานของฟังก์ชัน , False = ไม่แสดงข้อมูลการทำงานของฟังก์ชัน)

      ผลลัพธ์:
      - ถ้ายังไม่ถึงเวลาที่กำหนดจะคืนค่ากลับมาเป็น None
      - ถ้าถึงเวลาที่กำหนดแล้วจะคืนค่ากลับมาเป็น True.
      - ถ้า Error จะคีนค่ากลับมาเป็น False

      """
        return globals()['ATCV1_PY']['pyarmor__73'].pyarmor__112(timeout, showdb)