.text
main:
	li $s1, 15
	li $s2, 40
L0:
	la $t0, false
	ble $s2, $s1, jump_0
	la $t0, true
jump_0:
	la $t1, true
	beq $t1, $t0, if_label_0
L1:
	li $v0, 1
	la $a0, ($s2)
	syscall
	li $v0, 4
	la $a0, strinr_w
	syscall
	j end_
if_label_0:
	subu $t1, $s2, $s1
	move $s2, $t1
	j L0
end_:
.data
	true: .byte 1
	false: .byte 0
	strinr_w: .asciiz "\n" 
