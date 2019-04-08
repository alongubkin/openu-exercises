	.text

/* Switch from current_thread to next_thread. Make next_thread
 * the current_thread, and set next_thread to 0.
 * Use eax as a temporary register, which should be caller saved.
 */
	.globl thread_switch
	.globl current_thread
	.globl next_thread

thread_switch:
    pushal

	/* save current esp */
	movl current_thread, %eax
	movl %esp, (%eax)

	/* make next_thread the current_thread */
	movl next_thread, %eax
	movl %eax, current_thread

	/* set next_thread to NULL */
	movl $0, next_thread

	/* change to the active thread stack */
	movl (%eax), %esp

	popal
	ret				/* pop return address from stack */