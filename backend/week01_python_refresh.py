students = [
    {"id": "22000001", "name": "Nguyen Minh Anh", "major": "KHDL"},
    {"id": "22000002", "name": "Tran Duc Long", "major": "KHDL"},
    # Thêm sinh viên khác để khớp sĩ số hiện tại của các môn
    {"id": "22000003", "name": "Le Hoang Nam", "major": "KHDL"},
    {"id": "22000004", "name": "Pham Thi Mai", "major": "KHDL"},
]

courses = [
    {
        "code": "INT2204",
        "name": "Co so du lieu Web va he thong thong tin",
        "capacity": 3,
        "enrolled": 2,  # Đã có 2 SV (22000001 và 22000003), còn 1 chỗ -> Dùng cho TC01 (thành công) và TC02 (trùng)
    },
    {
        "code": "INT2205",
        "name": "Khai pha du lieu",
        "capacity": 2,
        "enrolled": 2,  # Đã đủ 2/2 chỗ (22000003 và 22000004) -> Dùng cho TC03 (lớp đầy)
    },
]

enrollments = [
    # Môn INT2204 (2 SV)
    {"student_id": "22000001", "course_code": "INT2204"},
    {"student_id": "22000003", "course_code": "INT2204"},
    # Môn INT2205 (2 SV - đầy lớp)
    {"student_id": "22000003", "course_code": "INT2205"},
    {"student_id": "22000004", "course_code": "INT2205"},
]

for course in courses:
    remaining = course["capacity"] - course["enrolled"]
    print(course["code"], "- con", remaining, "cho")
    
def find_course(course_code):
    for course in courses:
        if course["code"] == course_code:
            return course
    return None

def find_student(student_id):
    for student in students:
        if student["id"] == student_id:
            return student
    return None


#sửa lại hàm can_enroll so với ban đầu vì cần trả về nhiều thông tin hơn cho các test cases
def can_enroll(student_id, course_code):
    # 1. Kiểm tra sinh viên có tồn tại không
    if find_student(student_id) is None:
        return False, "Sinh vien khong ton tai"

    # 2. Kiểm tra học phần có tồn tại không
    course = find_course(course_code)
    if course is None:
        return False, "Hoc phan khong ton tai"

    # 3. Kiểm tra trùng lặp
    duplicated = any(
        item["student_id"] == student_id and item["course_code"] == course_code
        for item in enrollments
    )
    if duplicated:
        return False, "Sinh vien da dang ky hoc phan nay"
    
    # 4. Kiểm tra sĩ số lớp
    if course["enrolled"] >= course["capacity"]:
         return False, "Lop da du so luong"


    return True, "Co the dang ky"

try:
    limit = int(input("Nhap so luong hoc phan muon hien thi: "))
    print(courses[:limit])
except ValueError:
    print("So luong phai la so nguyen")
    
def search_courses(keyword):
    normalized = keyword.strip().lower()
    results = []
    
    for course in courses:
        code = course["code"].lower()
        name = course["name"].lower()
        if normalized in code or normalized in name:
            results.append(course)
    return results

def enroll_student(student_id, course_code):
    can_enroll_result, message = can_enroll(student_id, course_code)
    if not can_enroll_result:
        return False, message
    
    course = find_course(course_code)
    course["enrolled"] += 1
    enrollments.append({"student_id": student_id, "course_code": course_code})
    return True, "Dang ky hoc phan thanh cong"


# 3. Danh sách 5 trường hợp kiểm tra (Test Cases)
test_cases = [
    {
        "tc_id": "TC01",
        "name": "Đăng ký thành công",
        "student_id": "22000002",
        "course_code": "INT2204",
    },
    {
        "tc_id": "TC02",
        "name": "Đăng ký trùng",
        "student_id": "22000001",
        "course_code": "INT2204",
    },
    {
        "tc_id": "TC03",
        "name": "Lớp đầy",
        "student_id": "22000002",
        "course_code": "INT2205",
    },
    {
        "tc_id": "TC04",
        "name": "Mã học phần không tồn tại",
        "student_id": "22000001",
        "course_code": "INT9999",
    },
    {
        "tc_id": "TC05",
        "name": "Mã sinh viên không tồn tại",
        "student_id": "99999999",
        "course_code": "INT2204",
    },
]

#check test_cases
print("=" * 70)
print("TIẾN HÀNH KIỂM TRA CHƯƠNG TRÌNH ĐĂNG KÝ HỌC PHẦN")
print("=" * 70)

for tc in test_cases:
    print(f"\n[{tc['tc_id']}] Tình huống: {tc['name']}")
    print(f" -> Input: student_id='{tc['student_id']}', course_code='{tc['course_code']}'")
    actual_result = enroll_student(tc["student_id"], tc["course_code"])
    print(f" -> Kết quả quan sát được: {actual_result}")
    print("-" * 70)
