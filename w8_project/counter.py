#!/usr/bin/env python3
#
# @Filename:    counter.py
# @Author:      Yogesh K and Venkat K (Group 10)
# @Date:        27/01/2023
# @Description : A global counter that will increment
#and decrement by 1. Also handles overflow and underflow.

from pyteal import *
from pyteal.ast.bytes import Bytes
import program

UINT64_MAX = 0xFFFFFFFFFFFFFFFF


def approval_program():
    # globals

    global_owner  = Bytes("owner") # byteslice
    global_counter = Bytes("counter") # int

    op_increment = Bytes("inc")
    op_decrement = Bytes("dec")
    scratch_counter = ScratchVar(TealType.uint64)

    increment = Seq(
        scratch_counter.store(App.globalGet(global_counter)),
        #detect overflow
        If(
            scratch_counter.load() < Int(UINT64_MAX)
        )
        .Then(
            App.globalPut(global_counter, App.globalGet(global_counter) + Int(1)),
        ),
        Approve(),
    )
    decrement = Seq(
        scratch_counter.store(App.globalGet(global_counter)),
        #detect underflow
        If(
            scratch_counter.load() >Int(0)
        )
        .Then(
             App.globalPut(global_counter, scratch_counter.load() - Int(1))
        ),
        Approve(),
    )
    return program.event(
        init = Seq(
            App.globalPut(global_counter, Int(0)),
            App.globalPut(global_owner, Txn.sender()),
            Approve(),
        ),
        no_op =Cond(
            [Txn.application_args[0] == op_increment, increment],
            [Txn.application_args[0] == op_decrement, decrement],
            ),
    )


def clear_state_program():
    return Approve()
