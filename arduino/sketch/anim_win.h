// Animation: Animation
const uint32_t anim_win[][5] = {
    {0x00000010, 0x00000000, 0x00000000, 0x00000000, 130},  // Frame 1
    {0x00000010, 0x00800000, 0x00000000, 0x00000000, 130},  // Frame 1 (copy)_id2
    {0x00000010, 0x00800400, 0x00000000, 0x00000000, 130},  // Frame 1 (copy)_id3
    {0x00000010, 0x00800400, 0x20000000, 0x00000000, 130},  // Frame 1 (copy)_id4
    {0x00000010, 0x00800600, 0x20000000, 0x00000000, 130},  // Frame 1 (copy)_id5
    {0x00000010, 0x00a00600, 0x20000000, 0x00000000, 130},  // Frame 1 (copy)_id6
    {0x00000010, 0x00a00680, 0x20000000, 0x00000000, 130},  // Frame 1 (copy)_id7
    {0x00000010, 0x00a00680, 0x22000000, 0x00000000, 130},  // Frame 1 (copy)_id8
    {0x00000010, 0x00a006c0, 0x22000000, 0x00000000, 130},  // Frame 1 (copy)_id9
    {0x00000010, 0x00a806c0, 0x22000000, 0x00000000, 130},  // Frame 1 (copy)_id10
    {0x00000011, 0x00a806c0, 0x22000000, 0x00000000, 130},  // Frame 1 (copy) (copy)_id11
    {0x00000011, 0x40a806c0, 0x22000000, 0x00000000, 130},  // Frame 1 (copy) (copy)_id12
    {0x00000011, 0x40aa06c0, 0x22000000, 0x00000000, 130},  // Frame 1 (copy) (copy)_id13
    {0x00000011, 0x40aa06d0, 0x22000000, 0x00000000, 130},  // Frame 1 (copy) (copy)_id14
    {0x00000011, 0x40aa06d0, 0x22800000, 0x00000000, 130},  // Frame 1 (copy) (copy)_id15
    {0x00000011, 0x40aa06d0, 0x22a00000, 0x00000000, 130},  // Frame 1 (copy) (copy)_id16
    {0x00000011, 0x40aa06d4, 0x22a00000, 0x00000000, 130},  // Frame 1 (copy) (copy)_id17
    {0x00000011, 0x40aa86d4, 0x22a00000, 0x00000000, 130},  // Frame 1 (copy) (copy)_id18
    {0x00000011, 0x50aa86d4, 0x22a00000, 0x00000000, 130},  // Frame 1 (copy) (copy)_id19
    {0x00000011, 0x50aac6d4, 0x22a00000, 0x00000000, 130},  // Frame 1 (copy) (copy)_id20
    {0x00000011, 0x50aac6d5, 0x22a00000, 0x00000000, 130},  // Frame 1 (copy) (copy)_id21
    {0x00000011, 0x50aac6d5, 0x22a40000, 0x00000000, 130},  // Frame 1 (copy) (copy)_id22
    {0x00000011, 0x50aac6d5, 0xa2a40000, 0x00000000, 130},  // Frame 1 (copy) (copy)_id23
    {0x00000011, 0x50aad6d5, 0xa2a40000, 0x00000000, 130},  // Frame 1 (copy) (copy)_id24
    {0x00000011, 0x52aad6d5, 0xa2a40000, 0x00000000, 130},  // Frame 1 (copy) (copy)_id25
    {0x00000011, 0x52aad6d5, 0xa2a40000, 0x00000000, 130},  // Frame 1 (copy) (copy)_id26
    {0x00000011, 0x52aad6d5, 0xa2a40000, 0x00000000, 130},  // Frame 1 (copy) (copy)_id27
    {0x00000011, 0x52aad6d5, 0xa2a40000, 0x00000000, 130},  // Frame 1 (copy) (copy)_id28
    {0x00000011, 0x52aad6d5, 0xa2a40000, 0x00000000, 130},  // Frame 1 (copy) (copy)_id29
    {0x00000011, 0x52aad6d5, 0xa2a40000, 0x00000000, 130},  // Frame 1 (copy) (copy)_id30
    {0x00000011, 0x52aad6d5, 0xa2a40000, 0x00000000, 130},  // Frame 1 (copy) (copy)_id31
    {0x90900411, 0x52aad6d5, 0xa2a60001, 0x06000000, 130},  // Frame 1 (copy) (copy)_id32
    {0x90900411, 0x52aad6d5, 0xa2a60001, 0x06000000, 130},  // Frame 1 (copy) (copy)_id33
    {0x90900411, 0x52aad6d5, 0xa2a60001, 0x06000000, 130},  // Frame 1 (copy) (copy)_id34
    {0x249c4011, 0x52aad6d5, 0xa2a4204c, 0x18000000, 130},  // Frame 1 (copy) (copy)_id35
    {0x249c4011, 0x52aad6d5, 0xa2a4204c, 0x18000000, 130},  // Frame 1 (copy) (copy)_id36
    {0x249c4011, 0x52aad6d5, 0xa2a4204c, 0x18000000, 130},  // Frame 1 (copy) (copy)_id37
    {0x90900411, 0x52aad6d5, 0xa2a60001, 0x06000000, 130},  // Frame 1 (copy) (copy) (copy)
    {0x90900411, 0x52aad6d5, 0xa2a60001, 0x06000000, 130},  // Frame 1 (copy) (copy) (copy) (copy)
    {0x90900411, 0x52aad6d5, 0xa2a60001, 0x06000000, 130},  // Frame 1 (copy) (copy) (copy) (copy) (copy)
    {0x249c4011, 0x52aad6d5, 0xa2a4204c, 0x18000000, 130},  // Frame 44
    {0x249c4011, 0x52aad6d5, 0xa2a4204c, 0x18000000, 130},  // Frame 44 (copy)_id45
    {0x249c4011, 0x52aad6d5, 0xa2a4204c, 0x18000000, 130},  // Frame 44 (copy)_id46
    {0x90900411, 0x52aad6d5, 0xa2a60001, 0x06000000, 130},  // Frame 47
    {0x90900411, 0x52aad6d5, 0xa2a60001, 0x06000000, 130},  // Frame 47 (copy)_id48
    {0x90900411, 0x52aad6d5, 0xa2a60001, 0x06000000, 130},  // Frame 47 (copy)_id49
};
