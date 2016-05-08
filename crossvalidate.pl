#!/usr/bin/perl
use List::Util qw(sum);

# Configuration
$noFolds = 5;

# Command-line parameters
$inputDir = $ARGV[0];

# Read dataset
open (my $fh, '<', $inputDir . '/dataset-balanced.csv');
    my @lines = <$fh>;
    @lines = @lines[ 1 .. $#lines ]; #skip first line
close($fh);



# Cross-validation loop
for ($fold=0; $fold < $noFolds; $fold++) {
    # Open training and test file
    open (my $test_fh,     '>test-data-file-' . $fold .'.csv');
    open (my $training_fh, '>training-data-file-' . $fold . '.csv');

    # Separate training and test data according to fold
    $c=0;
    $tc=0;
    foreach $line (@lines) {
        if (($c - $fold) % 5 == 0) {
            # Test item, strip data to be predicted
            @fields = split(';', $line);
            $strip_line = $fields[0] . ';;;;;;;' . "\n";
            #$strip_line = $fields[1] . ';' . $fields[3] . ';' . $fields[4] . ';' . $fields[5] . ';' . $fields[6] . "\n";

            $performer[$tc] = $fields[1];
            $instrument[$tc] = $fields[3];
            $style[$tc] = $fields[4];
            $year[$tc] = $fields[5];
            $tempo[$tc] = $fields[6];

            print $test_fh $strip_line;
            $tc=$tc+1;
        }
        else {
            # Training item
            print $training_fh $line;
        }

        $c=$c+1;
    }

    # Close files
    close($test_fh);
    close($training_fh);

    # Run classifier
    system('python "Source/OptimusPrime.py" training-data-file-' . $fold .'.csv test-data-file-' .$fold . '.csv output-file-' . $fold . '.csv');

    # Compare outputs with data that was stripped
    open (my $fh, '<', 'output-file-' . $fold .'.csv');
    my @lines = <$fh>;
    @lines = @lines[ 1 .. $#lines ];

    # Keep score
    $c=0;
    for $line(@lines) {
        @field = split(';', $line);

        $performerPerformance[$fold] += !($field[1] eq $performer[$c]);
        $instrumentPerformance[$fold] += !($field[2] eq $instrument[$c]);
        $stylePerformance[$fold] += !($field[3] eq $style[$c]);
        $yearPerformance[$fold] += abs($field[4] - $year[$c]);
        $tempoPerformance[$fold] += abs($field[5] - $tempo[$c]);

        $c=$c+1;

    }
}


# Aggregate score
print "Error performance (lower is better)\n";
print "-----------------------------------\n";
print "Performer prediction\t" . join(';', @performerPerformance) . " => " . sum(@performerPerformance) ."\n";
print "Instrument prediction\t" . join(';', @instrumentPerformance) . " => " . sum(@instrumentPerformance) ."\n";
print "Style prediction\t" . join(';', @stylePerformance) . " => " . sum(@stylePerformance) ."\n";
print "Year prediction\t\t" . join(';', @yearPerformance) . " => " . sum(@yearPerformance) ."\n";
print "Tempo prediction\t" . join(';', @tempoPerformance) . " => " . sum(@tempoPerformance) ."\n";
