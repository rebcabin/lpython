program select_type1
implicit none
select type (uptr => iter%value())
    type is (integer)
        print *, iter%key(), ' = ', uptr
    type is (real)
        print *, iter%key(), ' = ', uptr
    type is (character(*))
        print *, iter%key(), ' = ', uptr
    type is (point)
        print *, iter%key(), ' = ', uptr
    class is (point2)
        print *, iter%key(), ' = ', uptr
    class default
        print *, iter%key(), ' = ', uptr
end select
end program
