from commands import send_command


def partition_output(conn):

    partition_start = 0x08
    num_partitions = 0x02
    command = f"\\P{chr(partition_start)}{chr(num_partitions)}/"
    send_command(conn, command)

#020d0a p2 armed
#000d0a all partitions off
#040d0a p3 armed
