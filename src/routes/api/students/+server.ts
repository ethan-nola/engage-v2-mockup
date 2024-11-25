import { json } from '@sveltejs/kit';
import { supabase } from '$lib/server/supabase';

export async function GET() {
    try {
        // Fetch students with their enrollments
        const { data, error } = await supabase
            .from('students')
            .select(`
                studentid,
                firstname,
                lastname,
                email,
                enrollments:enrollments (
                    enrollmentid,
                    enrollmentdate,
                    status,
                    classperiods:classperiods (
                        periodid,
                        periodname,
                        schedule,
                        courses:courses (
                            courseid,
                            coursename,
                            coursedescription
                        )
                    )
                )
            `);

        if (error) throw error;
        return json(data);
    } catch (error) {
        console.error('Error fetching students:', error);
        return json({ error: 'Failed to fetch students' }, { status: 500 });
    }
} 