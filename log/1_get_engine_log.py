# How to receive messages from the engine log system

import gs


def on_log(queue):
	for i in range(queue.GetSize()):
		msg = queue.GetMessage(i)
		prefix = queue.GetPrefix(i)
		details = queue.GetDetails(i)

		print('%s: %s' % ('Log' if prefix == '' else prefix, msg))
		if details != '':
			print('	%s' % details)


# disconnect the default log output
gs.GetOnLogSignal().DisconnectAll()

# hook the log signal to the on_log function
gs.GetOnLogSignal().Connect(on_log)

gs.log("This is a log.")
gs.log("This is a detailed log.", "Prefix", "Details")
gs.warn("This is a warning log.")
gs.error("This is an error log.")

# flush all queued log output
gs.FlushLog()

# disconnect from the signal
gs.GetOnLogSignal().DisconnectIs(on_log)

# we won't receive the following log entry
gs.log("This log won't be seen.")

# flush all queued log output (nothing gets printed out as there is no output connected)
gs.FlushLog()
