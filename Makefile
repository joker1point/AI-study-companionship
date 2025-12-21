CC = gcc
CFLAGS = -Wall -Wextra -g

# 源文件列表
SRCS = main.c login.c patient.c doctor.c medicine.c registration.c fee.c file.c

# 目标文件列表
OBJS = $(SRCS:.c=.o)

# 可执行文件名
TARGET = hospital_management_system

# 测试文件
TEST_SRC = test_hospital.c
TEST_TARGET = test_hospital

# 默认目标
all: $(TARGET)

# 编译可执行文件
$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^

# 编译目标文件
%.o: %.c hospital_management_system.h
	$(CC) $(CFLAGS) -c $<

# 编译测试文件
test: $(TEST_TARGET)

$(TEST_TARGET): $(TEST_SRC) $(filter-out main.o, $(OBJS))
	$(CC) $(CFLAGS) -o $@ $^

# 运行程序
run: $(TARGET)
	./$(TARGET)

# 运行测试
run_test: $(TEST_TARGET)
	./$(TEST_TARGET)

# 清理目标文件和可执行文件
clean:
	rm -f $(OBJS) $(TARGET) $(TEST_TARGET) *.o

.PHONY: all clean run test run_test
